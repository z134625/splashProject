# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SplashprojectItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    time = scrapy.Field()
    Forward = scrapy.Field()
    comment = scrapy.Field()
    fabulous = scrapy.Field()
