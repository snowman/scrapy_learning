import scrapy


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/']

    def parse(self, response):
        pass
