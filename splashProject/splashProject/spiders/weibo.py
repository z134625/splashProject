import scrapy
import itertools

from scrapy_splash import SplashRequest
from ..items import SplashprojectItem

lua_script = """
function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0

    local scroll_to = splash:jsfunc('window.scrollTo')
    local get_body_height = splash:jsfunc(
        'function() {return document.body.scrollHeight;}'
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
end
"""


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/?category=10007']

    def parse(self, response):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse_item, endpoint='execute',
                                args={'lua_source': lua_script, 'wait': 6})

    def parse_item(self, response):
        items = SplashprojectItem()
        info = response.css('.WB_frame_c .pt_ul .UG_list_a')
        for item in info:
            author = item.css('.subinfo_box a span::text').extract_first()
            time = item.xpath('.//div[@class="subinfo_box clearfix"]/span/text()').extract_first()
            Forward = item.xpath('.//div[@class="subinfo_box clearfix"]/span[6]/em[2]/text()').extract_first()
            comment = item.xpath('.//div[@class="subinfo_box clearfix"]/span[4]/em[2]/text()').extract_first()
            fabulous = item.xpath('.//div[@class="subinfo_box clearfix"]/span[2]/em[2]/text()').extract_first()
            writing = item.css('.list_title_s div::text').re(r'\S')
            items['author'] = author
            items['time'] = time
            items['Forward'] = Forward
            items['comment'] = comment
            items['fabulous'] = fabulous
            items['writing'] = "".join(itertools.chain(*writing))
            yield items
