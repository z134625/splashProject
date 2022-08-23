import scrapy
import re

from ..items import DazongdianpingItem
from scrapy_splash import SplashRequest
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

cookies = {'cookie': 's_ViewType=10; _lxsdk_cuid=17b017f8affc8-06f71231a8e514-7e687969-144000-17b017f8affc8; _lxsdk=17b017f8affc8-06f71231a8e514-7e687969-144000-17b017f8affc8; _hc.v=8270d4a8-5009-12b5-65c9-a6c95630194c.1627898161; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1627817742,1627865443,1627898071; ctu=49c636057a583d1f092f0432f113a3cbf82e3cf867dc15925f01fa2fe48d1a0b; fspop=test; cy=1609; cye=shuangliu; ll=7fd06e815b796be3df069dec7836c3df; ua=13882363117; dplet=7c601930e9f6825f2bd8b47950283b0d; dper=afd4096b02e3d4e0819657b39b2b405754f362d41916b717281d093237fa372c32890e7650d14872bd72191c27edfe1f38ce739e8cbb4e4319a5617fdca9c3227e06117502d74375b2faf055bea7b6c2404180e455c89f81fa24e31d03a36937; _lxsdk_s=17b06689eb5-5cc-5d3-15||466; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1627905222'}


class DazongSpider(scrapy.Spider):
    name = 'dazong'
    allowed_domains = ['dianping.com']
    base_url = 'http://www.dianping.com/chengdu/ch30/g134'

    def start_requests(self):
        yield SplashRequest(self.base_url, cookies=cookies, callback=self.parse, endpoint='execute',  args={"lua_source": lua_script, 'wait': 6}, cache_args=['lua_source'])

    def parse(self, response):
        urls = [f'p{n}' for n in range(1, 51)]
        for url in urls:
            new_url = self.base_url + url
            yield SplashRequest(new_url, cookies=cookies, callback=self.parse_item, endpoint='execute',  args={"lua_source": lua_script, 'wait': 6}, cache_args=['lua_source'])

    def parse_item(self, response):
        item = DazongdianpingItem()
        info = response.xpath('//*[@id="shop-all-list"]/ul/li')
        for ite in info:
            name = ite.xpath('./div[@class="txt"]/div[1]/a/h4/text()').extract_first()
            comment = ite.xpath('.//div[@class="comment"]/a[1]/b').re_first(r'<b>.*?</b>', re.S)
            price = ite.xpath('.//div[@class="comment"]/a[2]/b').re_first(r'<b>.*?</b>', re.S)
            address = ite.xpath('.//div[@class="tag-addr"]/a[2]/span').re_first(r'<span.*?</span>', re.S)
            item['name'] = name
            item['comment'] = comment
            item['price'] = price
            item['address'] = address
            yield item

