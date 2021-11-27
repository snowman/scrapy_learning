# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 使用 Python 字典 存储 一本书 的 信息 有 以下 缺点:
#
# 1. 无法一目了然地了解数据中包含哪些字段, 影响代码可读性
# 2. 缺乏对字段名字的检测, 容易因程序员的笔误而出错
# 3. 不便于携带元数据(传递给其他组件的信息)
#
# 为 解决 上述 问题, 在 Scrapy 中 可以 使用 自定义 的 Item 类 封装

from scrapy import Item, Field
class BookItem(Item):
    name = Field()
    price = Field()

# >>> book1 = BookItem(name='Needful Things', price=45.0)
# >>> book1
# {'name': 'Needful Things', 'price': 45.0}
#
# >>> book2 = BookItem()
# >>> book2
# {}
#
# >>> book2['name'] = 'Life of Pi'
# >>> book2['price'] = 32.5
# >>> book2
# {'name': 'Life of Pi', 'price': 32.5}

# prevent typo
#
# >>> book = BookItem()
# >>> book['name'] = 'Memoirs of a Geisha'
# >>> book['prize'] = 43.0 # typo
# Traceback (most recent call last):
# ...
# KeyError: 'BookItem does not support field: prize'

# acess
#
# >>> book = BookItem(name='Needful Things', price=45.0)
# >>> book['name']
# 'Needful Things'
# >>> book.get('price', 60.0)
# 45.0
# >>> list(book.items())
# [('price', 45.0), ('name', 'Needful Things')]

class ForeignBookItem(BookItem):
    translator = Field()
