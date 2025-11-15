BOT_NAME = "jobs_spider"
SPIDER_MODULES = ["jobs_spider.spiders"]
NEWSPIDER_MODULE = "jobs_spider.spiders"

DOWNLOADER_MIDDLEWARES = {
    "scrapy_playwright.middleware.ScrapyPlaywrightDownloadHandler": 543,
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1  # adjust according to target
CONCURRENT_REQUESTS = 8

ITEM_PIPELINES = {
    "jobs_spider.pipelines.SQLitePipeline": 300,
}