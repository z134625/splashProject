# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DazongdianpingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    comment = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()

