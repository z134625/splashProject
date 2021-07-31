# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class VideoSpiderPipeline:
    def __init__(self):
        self.name = set()

    def process_item(self, item, spider):
        name = item['video_title']
        if name in self.name:
            raise DropItem('重复数据:%s' % name)
        self.name.add(name)
        return item
