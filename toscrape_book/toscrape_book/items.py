# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ToscrapeBookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BookDetailItem(scrapy.Item):
    name          = scrapy.Field()
    price         = scrapy.Field()
    review_rating = scrapy.Field() # range from [1, 5]
    review_num    = scrapy.Field()
    upc           = scrapy.Field() # Universal Product Code
    stock         = scrapy.Field()
