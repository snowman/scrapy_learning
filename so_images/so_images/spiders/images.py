import scrapy
from scrapy import Request
from ..items import ImageItem
import json


class ImagesSpider(scrapy.Spider):
    BASE_URL = 'https://image.so.com/zjl?ch=art&sn=%s'
    start_index = 0

    # prevent consuming huge disk
    MAX_DOWNLOAD_NUM = 1000

    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = [BASE_URL % 0]

    def parse(self, response):
        image = ImageItem()

        infos = json.loads(response.body.decode('utf-8'))

        image['image_urls'] = [info['qhimg_url'] for info in infos['list']]

        yield image

        self.start_index += infos['count']

        if infos['count'] > 0 and self.start_index < self.MAX_DOWNLOAD_NUM:
            yield Request(self.BASE_URL % self.start_index)
