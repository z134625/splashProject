import scrapy
import re
import time
import os
import requests

from ..settings import FILES_STORE
from scrapy_splash import SplashRequest
from ..items import VideolispiderItem

lua_script1 = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(1))
  return splash:html()
end
"""

lua_script = """
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(1))
  js = string.format("document.querySelector('.listloadmore a').click();", args.page)
  splash:runjs(js)
  assert(splash:wait(1))
  return splash:html()
end
"""


class PearvideoSpider(scrapy.Spider):
    name = 'pearvideo'
    allowed_domains = ['pearvideo.com']
    base_urls = ['https://www.pearvideo.com/category_59']

    def start_requests(self):
        for url in self.base_urls:
            time.sleep(0.5)
            yield SplashRequest(url, callback=self.parse, endpoint='execute',
                                args={'lua_source': lua_script, 'wait': 1})

    def parse(self, response):
        urls = response.xpath('//li[@class="categoryem"]')
        for url in urls:
            url = url.css('.vervideo-bd a::attr(href)').extract_first()
            new_url = 'https://www.pearvideo.com/' + str(url)
            time.sleep(0.5)
            yield SplashRequest(new_url, callback=self.parse_video, endpoint='execute',
                                args={'lua_source': lua_script1, 'wait': 1})

    def parse_video(self, response):
        item = VideolispiderItem()
        title = response.xpath('//*[@id="detailsbd"]/div[1]/div[2]/div/div[1]/h1/text()').extract_first()
        likes = response.xpath('//*[@id="detailsbd"]/div[1]/div[2]/div/div[1]/div/div[1]/text()').re_first(r'\d', re.S)
        author = response.xpath('//*[@id="detailsbd"]/div[1]/div[3]/div[1]/div[1]/a/div/text()').re_first(r'\S')
        video_url = response.xpath('//*[@id="JprismPlayer"]/video/@src').extract_first()
        item['title'] = title
        item['likes'] = likes
        item['author'] = author
        item['video_url'] = video_url
        yield item
