import json
from datetime import datetime
from typing import Dict, Optional

import scrapy
from scrapy import Selector
from scrapy.http import Request
from scrapy_playwright.page import PageMethod

from ...items import JobItem

# import library
class TopCVSpider(scrapy.Spider):
    """Scrape TopCV listing pages and persist normalized job data."""

    name = "topcv_jobs"
    allowed_domains = ["topcv.vn"]
    start_urls = ["https://www.topcv.vn/tim-viec-lam-moi-nhat"]

    _REQUEST_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/129.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.7"
        ),
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.topcv.vn/",
    }

    def __init__(self, max_pages: int = 1, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_pages = max(1, int(max_pages))

    # ---------------------------------------------------------------------
    # Request helpers
    # ---------------------------------------------------------------------
    def start_requests(self):
        yield Request(
            self.start_urls[0],
            headers=self._REQUEST_HEADERS,
            meta=self._playwright_meta(page_number=1),
        )

    def _playwright_meta(self, page_number: int) -> Dict[str, object]:
        return {
            "playwright": True,
            "playwright_context_kwargs": {
                "user_agent": self._REQUEST_HEADERS["User-Agent"],
                "locale": "vi-VN",
            },
            "playwright_page_methods": [
                PageMethod("wait_for_load_state", "networkidle"),
                PageMethod("wait_for_timeout", 750),
            ],
            "page_number": page_number,
        }

    # ------------------------------------------------------------------
    # Listing parsing
    # ------------------------------------------------------------------
    def parse(self, response: scrapy.http.Response, **kwargs):
        page_number = response.meta.get("page_number", 1)
        cards = response.css("div.job-item-search-result")

        if not cards:
            self.logger.warning("No job cards found on %s", response.url)

        for card in cards:
            summary = self._parse_listing_card(card, response)
            if not summary.get("url"):
                continue

            meta = {
                "summary": summary,
                "playwright": True,
                "playwright_context_kwargs": {
                    "user_agent": self._REQUEST_HEADERS["User-Agent"],
                    "locale": "vi-VN",
                },
                "playwright_page_methods": [
                    PageMethod("wait_for_load_state", "networkidle"),
                    PageMethod("wait_for_timeout", 500),
                ],
            }

            yield response.follow(
                summary["url"],
                callback=self.parse_detail,
                headers=self._REQUEST_HEADERS,
                meta=meta,
            )

        next_href = response.css('.box-pagination a[rel="next"]::attr(data-href)').get()
        if next_href and page_number < self.max_pages:
            next_url = response.urljoin(next_href)
            yield Request(
                next_url,
                callback=self.parse,
                headers=self._REQUEST_HEADERS,
                meta=self._playwright_meta(page_number=page_number + 1),
                dont_filter=True,
            )

    def _parse_listing_card(self, card: Selector, response: scrapy.http.Response) -> Dict[str, Optional[str]]:
        def _clean(value: Optional[str]) -> Optional[str]:
            return value.strip() if value and value.strip() else None

        url = card.css(".title-block a::attr(href)").get()
        if url:
            url = response.urljoin(url)

        title = card.css(".title-block a span::text").get() or card.css(".title-block a::text").get()
        company = card.css("a.company span.company-name::text").get()
        salary = card.css(".info label.salary span::text").get()
        location = card.css(".info label.address span.city-text::text").get()
        experience = card.css(".info label.exp span::text").get()
        tags = [tag.strip() for tag in card.css(".box-icon a.item-tag::text").getall() if tag.strip()]

        return {
            "url": url,
            "title": _clean(title),
            "company": _clean(company),
            "salary": _clean(salary),
            "location": _clean(location),
            "experience": _clean(experience),
            "tags": tags,
        }

    # ------------------------------------------------------------------
    # Detail parsing
    # ------------------------------------------------------------------
    def parse_detail(self, response: scrapy.http.Response):
        summary = response.meta.get("summary", {})
        item = JobItem()

        item["url"] = response.url.split("?")[0]
        item["title"] = summary.get("title")
        item["company"] = summary.get("company")
        item["salary"] = summary.get("salary")
        item["location"] = summary.get("location")
        item["experience"] = summary.get("experience")
        item["tags"] = summary.get("tags") or []
        item["skills"] = None

        job_data = self._extract_job_posting(response)
        if job_data:
            experience = job_data.get("experienceRequirements")
            if isinstance(experience, str) and experience.strip():
                item["experience"] = experience.strip()

            salary_text = self._format_salary(job_data.get("baseSalary"))
            if salary_text:
                item["salary"] = salary_text

            location_text = self._format_location(job_data.get("jobLocation"))
            if location_text:
                item["location"] = location_text

            description_html = job_data.get("description", "")
            if description_html:
                item["description"] = self._html_to_text(description_html)

            skills = job_data.get("skills")
            if isinstance(skills, list):
                item["skills"] = [skill.strip() for skill in skills if isinstance(skill, str) and skill.strip()]
            elif isinstance(skills, str) and skills.strip():
                item["skills"] = skills.strip()

        if not item.get("description"):
            fallback_parts = [
                text.strip()
                for text in response.css(".job-description__item--content ::text").getall()
                if text.strip()
            ]
            item["description"] = "\n".join(fallback_parts)

        item["scraped_at"] = datetime.utcnow().isoformat()
        yield item

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    def _extract_job_posting(self, response: scrapy.http.Response) -> Optional[dict]:
        scripts = response.xpath('//script[@type="application/ld+json"]/text()').getall()
        for raw in scripts:
            if not raw:
                continue
            raw = raw.strip()
            if not raw:
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                continue
            job = self._select_jobposting(data)
            if job:
                return job
        return None

    def _select_jobposting(self, data) -> Optional[dict]:
        if isinstance(data, dict):
            if data.get("@type") == "JobPosting":
                return data
        elif isinstance(data, list):
            for entry in data:
                job = self._select_jobposting(entry)
                if job:
                    return job
        return None

    def _format_salary(self, base_salary: Optional[dict]) -> Optional[str]:
        if not isinstance(base_salary, dict):
            return None

        value = base_salary.get("value")
        if not isinstance(value, dict):
            return None

        min_value = value.get("minValue")
        max_value = value.get("maxValue")
        currency = base_salary.get("currency")
        unit = value.get("unitText")

        def _fmt(number: Optional[float]) -> Optional[str]:
            if number is None:
                return None
            try:
                return f"{float(number):,.0f}"
            except (TypeError, ValueError):
                return str(number)

        parts = []
        min_part = _fmt(min_value)
        max_part = _fmt(max_value)

        if min_part and max_part and min_part != max_part:
            parts.append(f"{min_part}-{max_part}")
        elif max_part:
            parts.append(f"≤ {max_part}")
        elif min_part:
            parts.append(f"≥ {min_part}")

        if currency:
            parts.append(currency)

        if isinstance(unit, str):
            parts.append(unit.lower())

        return " ".join(parts) if parts else None

    def _format_location(self, location_data) -> Optional[str]:
        if isinstance(location_data, list):
            parts = [self._format_location(entry) for entry in location_data]
            parts = [part for part in parts if part]
            return ", ".join(dict.fromkeys(parts)) if parts else None

        if not isinstance(location_data, dict):
            return None

        address = location_data.get("address") or {}
        if not isinstance(address, dict):
            return None

        components = []
        for key in ("streetAddress", "addressLocality", "addressRegion", "addressCountry"):
            value = address.get(key)
            if isinstance(value, str) and value.strip():
                components.append(value.strip())

        return ", ".join(components) if components else None

    def _html_to_text(self, html: str) -> str:
        if not html:
            return ""

        selector = Selector(text=html)
        lines = []
        for node in selector.xpath('//*[self::h2 or self::h3 or self::h4 or self::p or self::li]'):
            text_parts = [
                segment.strip()
                for segment in node.xpath('.//text()').getall()
                if segment.strip()
            ]
            if not text_parts:
                continue
            text = " ".join(text_parts)
            tag = getattr(node.root, "tag", None)
            if tag == "li":
                text = f"- {text}"
            lines.append(text)

        if not lines:
            fallback = [piece.strip() for piece in selector.xpath('//text()').getall() if piece.strip()]
            lines = fallback

        return "\n".join(lines)
