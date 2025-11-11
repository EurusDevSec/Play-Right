import scrapy 
from ...items import JobItem
import datetime


class JobSpider(scrapy.Spider):
    name="jobs"
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = JobItem()
            item['url'] = response.urljoin(quote.css('span a::attr(href)').get())
            item['title'] = quote.css('span.text::text').get()
            item['company'] = quote.css('small.author::text').get() # Giả sử author là company
            item['location'] = 'N/A'
            item['description'] = item['title']
            item['scraped_at'] = datetime.datetime.utcnow().isoformat()
            yield item
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)
