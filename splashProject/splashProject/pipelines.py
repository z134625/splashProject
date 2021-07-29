# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class SplashprojectPipeline:
    def __init__(self):
        self.author = set()

    def process_item(self, item, spider):
        author = item['author']
        if author in self.author:
            raise DropItem('重复数据:%s' % author)
        self.author.add(author)
        return item
