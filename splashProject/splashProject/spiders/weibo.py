import scrapy

from scrapy_splash import SplashRequest
from ..items import SplashprojectItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/?category=10007']

    def parse(self, response):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse_item, endpoint='')

    def parse_item(self, response):
        item = SplashprojectItem()
