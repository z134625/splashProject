import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ScrapyOneItem


class ParkSpider(CrawlSpider):
    name = 'park'
    # allowed_domains = ['xxxx.com']
    start_urls = ['https://wz.sun0769.com/political/index/politicsNewest']
    link = LinkExtractor(allow=r'id=1&page=\d+')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = ScrapyOneItem()
        links = response.xpath('/html/body/div[2]/div[3]/ul[2]/li')
        for li in links:
            title = li.xpath('./span[3]/a/text()').extract_first()
            status = li.xpath('./span[2]/text()').re_first(r'\S+')
            time = li.xpath('./span[5]/text()').re_first(r'\S+')
            info_url = li.xpath('./span[3]/a/@href').extract_first()
            item['title'] = title
            item['status'] = status
            item['time'] = time
            new_url = 'https://wz.sun0769.com' + info_url
            yield scrapy.Request(new_url, callback=self.parse_info, meta={'item': item})

    def parse_info(self,response):
        item = response.meta['item']
        text = response.xpath('/html/body/div[3]/div[2]/div[2]/div[2]/pre/text()').extract_first()
        item['text'] = text
        print(item)
        yield item

