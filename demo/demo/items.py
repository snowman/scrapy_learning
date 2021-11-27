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
# >>> from itemadapter import ItemAdapter
# >>> list(ItemAdapter(book2).keys())
# []
# >>> list(ItemAdapter(book2).field_names())
# ['name', 'price']
#
# >>> book2['name'] = 'Life of Pi'
# >>> list(ItemAdapter(book2).keys())
# ['name']
# >>> book2['price'] = 32.5
# >>> list(ItemAdapter(book2).keys())
# ['name', 'price']
#
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

class ExampleItem(Item):
    x = Field(a='hello', b=[1, 2, 3]) # x has two meta data, a is string, b is list
    y = Field(a=lambda x: x ** 2)     # y has one meta data, a function

# >>> e = ExampleItem(x=100, y=200)
# >>> e.fields
# {
#   'x': {'a': 'hello', 'b': [1, 2, 3]},
#   'y': {'a': <function __main__.ExampleItem.<lambda>>}
# }
#
# >>> type(e.fields['x'])
# scrapy.item.Field
#
# >>> type(e.fields['y'])
# scrapy.item.Field
#
# >>> issubclass(Field, dict)
# True
#
# NOTE, don't confused "e.fields['x']" with "e['x']"
#   e.fields['x'] is meta data of field x
#   e.['x']       is data
#
# >>> field_x = e.fields['x']
# >>> field_x
# {'a': 'hello', 'b': [1, 2, 3]}
# >>> field_x['a']
# 'hello'
#
# >>> field_y = e.fields['y']
# >>> field_y
# {'a': <function __main__.ExampleItem.<lambda>>}
# >>> field_y.get('a', lambda x: x)
# <function __main__.ExampleItem.<lambda>>

# >>> book['authors'] = ['李雷', '韩梅梅', '吉姆']
# 在 写入 CSV 文件 时, 需要 将 列表 内 所有 字符串 串行化 成 一个 字符串
# 串行化 的 方式 有 很多种, 例如:
#
# "李雷|韩梅梅|吉姆"            # '|'.join(book['authors'])
# "李雷;韩梅梅;吉姆"            # ';'.join(book['authors'])
# "['李雷', '韩梅梅', '吉姆']"  # str(book['authors'])

# 元数据 键 serializer 是 CsvItemExporter 规定的
# 它会用 该 键 获取 元数据, 即一个 串行化 函数 对象, 并 使用 这个 串行化 函数
# 将 authors 字段 串行化 成 一个 字符串
class BookItem2(Item):
    authors = Field(serializer=lambda x: '|'.join(x))
