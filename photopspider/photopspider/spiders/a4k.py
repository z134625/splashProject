import scrapy
import time

from ..items import PhotopspiderItem


class A4kSpider(scrapy.Spider):
    name = 'a4k'
    allowed_domains = ['pic.netbian.com']
    base_urls = [f'https://pic.netbian.com//4kmeinv/index_{n}.html' for n in range(1, 146)]

    def start_requests(self):
        for url in self.base_urls:
            time.sleep(0.5)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = PhotopspiderItem()
        images = response.css('.slist .clearfix li')
        for image in images:
            image_url = image.css('a img::attr(src)').extract_first()
            image_title = image.css('a b::text').extract_first()
            item['title'] = image_title
            item['image_url'] = 'https://pic.netbian.com/' + image_url
            yield item
