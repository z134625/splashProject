# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy import Item
from pymongo import MongoClient


class SplashprojectPipeline:
    def __init__(self):
        self.author = set()

    def process_item(self, item, spider):
        author = item['author']
        if author in self.author:
            raise DropItem('重复数据:%s' % author)
        self.author.add(author)
        return item


class MongdbPipeline:
    def open_spider(self, spider):
        db_url = spider.settings.get('MONGODB_URL')
        db = spider.settings.get('MONGODB_NAME')
        self.db_client = MongoClient(db_url)
        self.db = self.db_client[db]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_item(item)
        return item

    def insert_item(self, item):
        if isinstance(item, Item):
            item = dict(item)
        self.db.weibo.insert_one(item)
