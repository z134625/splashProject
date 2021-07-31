import scrapy
import json

from scrapy_splash import SplashRequest
from ..items import VideoSpiderItem

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


class DouyinSpider(scrapy.Spider):
    name = 'douyin'
    allowed_domains = ['douyin.com']
    start_urls = ['https://www.douyin.com/aweme/v1/web/search/item/?device_platform=webapp&aid=6383&channel'
                  '=channel_pc_web&search_channel=aweme_video_web&sort_type=0&publish_time=0&keyword=%E7%BE%8E%E5%A5'
                  '%B3&search_source=normal_search&query_correct_type=1&is_filter_search=0&offset=0&count=24'
                  '&version_code=160100&version_name=16.1.0&cookie_enabled=true&screen_width=1536&screen_height=864'
                  '&browser_language=zh-CN&browser_platform=Win32&browser_name=Mozilla&browser_version=5.0+('
                  'Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,'
                  '+like+Gecko)+Chrome%2F92.0.4515.107+Safari%2F537.36+Edg%2F92.0.902.55&browser_online=true'
                  '&_signature=_02B4Z6wo00f01sC7l0QAAIDDo7FXLXEj6IbAu5PAANE48d']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_html = json.load(response)
        urls = json_html.get('data')
        for url in urls:
            url.get('aweme_info').get('aweme_id')
            new_url = 'https://www.douyin.com/video/'+url

    def parse_html(self, response):
        item = VideoSpiderItem()
        author = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div['
                                '2]/a/div/span/span/span/span/span/text()').extract_first()

        fans = response.xpath(
            '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/p/span[2]/text()').extract_first()
        likes = response.xpath(
            '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/p/span[4]/text()').extract_first()
        video_likes = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div['
                                     '1]/span/text()').extract_first()
        video_comment = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div['
                                       '2]/span/text()').extract_first()
        video_title = response.xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/h1/span[2]/span['
                                     '1]/span/span/span/text()').extract_first()
        item['author'] = author
        item['likes'] = likes
        item['fans'] = fans
        item['video_likes'] = video_likes
        item['video_comment'] = video_comment
        item['video_title'] = video_title
        yield item
