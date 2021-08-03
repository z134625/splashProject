# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy import Item
from scrapy.exceptions import DropItem


class ScrapyOnePipeline:
    def __init__(self):
        self.title = set()

    def process_item(self, item, spider):
        title = item['title']
        if title in self.title:
            raise DropItem('重复内容{0}'.format(title))
        self.title.add(title)
        return item


class MongodbPipeline:
    def open_spider(self,spider):
        db_url = spider.settings.get('MONGODB_URL')
        db_name = spider.settings.get('MONGODB_NAME')
        self.db_client = MongoClient(db_url)
        self.db = self.db_client[db_name]

    def process_item(self, item, spider):
        if isinstance(item, Item):
            item = dict(item)
        self.db.info.insert_one(item)
        return item

    def close_spider(self, spider):
        self.db_client.close()