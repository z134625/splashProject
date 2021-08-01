# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideolispiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    likes = scrapy.Field()
    author = scrapy.Field()
    video_url = scrapy.Field()