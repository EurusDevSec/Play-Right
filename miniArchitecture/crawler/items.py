import scrapy


class JobItem(scrapy.Item):
    """Normalized representation of a single job posting."""

    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    tags = scrapy.Field()
    skills = scrapy.Field()
    description = scrapy.Field()
    scraped_at = scrapy.Field()