# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VideoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    author = scrapy.Field()
    fans = scrapy.Field()
    likes = scrapy.Field()
    video_title = scrapy.Field()
    video_likes = scrapy.Field()
    video_comment = scrapy.Field()

