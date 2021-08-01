# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from scrapy import Item
from scrapy.pipelines.images import ImagesPipeline
from .settings import IMAGE_PATH

class PhotopspiderPipeline:
    def __init__(self):
        self.url = set()

    def process_item(self, item, spider):
        url = item['image_url']
        if url in self.url:
            raise DropItem('重复图片')
        self.url.add(url)
        return item


class MongodbPipeline:
    def open_spider(self, spider):
        db_url = spider.settings.get('MONGODB_URL')
        db_name = spider.settings.get('MONGDB_NAME')
        self.db_client = MongoClient(db_url)
        self.db = self.db_client[db_name]

    def close_spider(self,spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_mogo(item)
        return item

    def insert_mogo(self, item):
        if isinstance(item, Item):
            item = dict(item)
        return self.db.photo.insert_one(item)


class PhotospiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url = item['image_url']
        yield scrapy.Request(url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        title = request.meta['item']['title']
        file_path = u'{0}/{1}.jpg'.format(IMAGE_PATH, title)
        return file_path

