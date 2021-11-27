# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class DemoPipeline:
    def process_item(self, item, spider):
        return item

class PriceConverterPipeline(object):
    # 英镑 兑换 人民币 汇率
    exchange_rate = 8.5309

    # If process_item returns data (Item or dict),
    # the return data will relay to next Item Pipeline

    # If process_item raise DropItem Exception (scrapy.exceptions.DropItem),
    # the item will be drop, and never relayt to following Item Pipeline processing,
    # neither will export to file

    # 通常, 在 检测 到 无效数据 或 过滤数据 时, 抛出 DropItem 异常
    def process_item(self, item, spider):
        # 提取 item 的 price 字段 (如 ￡53.74)
        # 去掉 前面 英镑 符号￡, 转换为 float 类型, 乘以汇率
        price = float(item['price'][1:]) * self.exchange_rate

        # 保留 2 位小数, 赋值回 item 的 price 字段
        item['price'] = '￥ %.2f' % price

        return item

    # open_spider(self, spider)
    # Spider 打开时 (处理数据前) 回调, 通常 用于 在 开始 处理 数据 之前, 完成 某些 初始化 工作, 如 连接 数据库

    # close_spider(self, spider)
    # Spider 关闭时 (处理数据后) 回调, 通常 用于 在 处理 完 所有数据 之后, 完成 某些 清理 工作, 如 关闭 数据库

    # from_crawler(cls, crawler)
    # 创建 Item Pipeline 对象时 回调. 通常 用于 读取 配置 crawler.settings, 根据 配置 创建 Item Pipeline 对象

# 以 书名 作为 主键 (实际 应以 ISBN 编号 为 主键, 但是 仅 爬取 了 书名 和 价格) 进行 去重
from scrapy.exceptions import DropItem

class DuplicatesPipeline(object):
    def __init__(self):
        self.book_set = set()

    def process_item(self, item, spider):
        name = item['name']

        if name in self.book_set:
            raise DropItem("Duplicate book found: %s" % item)

        self.book_set.add(name)

        return item
