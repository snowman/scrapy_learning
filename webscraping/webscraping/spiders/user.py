import scrapy
from scrapy.http import Request, FormRequest
from ..items import UserItem


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['127.0.0.1']
    start_urls = ['http://127.0.0.1:8000/places/default/user/profile']

    def parse(self, response):
        user = UserItem()

        keys = response.css('table label::text').re('(.+):')
        values = response.css('table td.w2p_fw::text').extract()
        item = dict(zip(keys, values))

        # yield item

        user['first_name'] = values[0]
        user['last_name'] = values[1]
        user['email'] = values[2]

        yield user

    login_url = 'http://127.0.0.1:8000/places/default/user/login'

    def start_requests(self):
        # override base's start_requests method, so UserSpider.parse would not callback
        yield Request(self.login_url, callback=self.login)

    def login(self, response):
        fd = {'email': 'liushuo@webscraping.com', 'password': '123456'}

        yield FormRequest.from_response(response, formdata=fd,
                                        callback=self.parse_login)

    def parse_login(self, response):
        if 'Welcome Liu' in response.text:
            # call base start_requests method, so UserSpider.parse will be callback
            yield from super().start_requests()    # Python 3 语法
