import scrapy 
from ...items import JobItem
import datetime


class JobSpider(scrapy.Spider):
    name="jobs"
    start_urls = ["https://quotes.toscrape.com/"]

    