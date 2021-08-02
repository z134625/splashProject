# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from fontTools.ttLib import TTFont
from .settings import woff_str_601
from bs4 import BeautifulSoup


class DazongdianpingPipeline:
    def process_item(self, item, spider):
        address = item['address']
        price = item['price']
        comment = item['comment']
        item['address'] = str(self.unicode_item(address))
        item['price'] = '人均' + str(self.unicode_item(price))
        item['comment'] = str(self.unicode_item(comment)) + '条评价'
        return item

    def unicode_item(self, info):
        info = repr(info).replace(r'\u', 'uni')
        if 'tagName' in info:
            return self.info_name('tagName', info)
        elif 'shopNum' in info:
            return self.info_name('shopNum', info)

    def info_name(self, path, info):
        font = TTFont('./'+path+'.woff')
        woff_unicode = font['cmap'].tables[0].ttFont.getGlyphOrder()
        woff_character = ['.notdef', 'x'] + list(woff_str_601)
        woff_dict = dict(zip(woff_unicode, woff_character))
        html = ''
        for key in woff_dict:
            if key in info:
                html = info.replace(r'%s' % str(key), str(woff_dict[key]))
                info = html
        soup = BeautifulSoup(html, 'lxml')
        return soup.text