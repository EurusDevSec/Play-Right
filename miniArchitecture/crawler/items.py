import scrapy
class JobItem(scrapy.Item):
    url = scrapy.Field()
    title=scrapy.Field()
    company=scrapy.Field()
    location=scrapy.Field()
    salary=scrapy.Field()
    description=scrapy.Field()
    scraped_at=scrapy.Field()