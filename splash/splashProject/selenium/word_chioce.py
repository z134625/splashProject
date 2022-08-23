# @File  : word_chioce.py
# @Author: Park boy
# @Date  : 2021-08-03
from fontTools.ttLib import TTFont
# from bs4 import BeautifulSoup
import csv
from word_setting import woff_str_601

def process_item(item):
    address = item['address']
    price = item['price']
    comment = item['comment']
    item['address'] = str(unicode_item(address, True))
    item['price'] = '人均' + str(unicode_item(price, False))
    item['comment'] = str(unicode_item(comment, False)) + '条评价'
    return item


def unicode_item(info, n):
    info = repr(info).replace(r'\u', 'uni')
    if n:
        return info_name('tagName', info)
    else:
        return info_name('shopNum', info)


def info_name(path, info):
    font = TTFont('./' + path + '.woff')
    woff_unicode = font['cmap'].tables[0].ttFont.getGlyphOrder()
    woff_character = ['.notdef', 'x'] + list(woff_str_601)
    woff_dict = dict(zip(woff_unicode, woff_character))
    html = ''
    for key in woff_dict:
        if key in info:
            html = info.replace(r'%s' % str(key), str(woff_dict[key]))
            info = html

    return html


if __name__ == '__main__':
    pass
    item = {'name': '彭镇老茶馆', 'comment': '\uf5f8\uf7e01', 'price': '￥11', 'address': '\uf1a9\uf152'}
    item = process_item(item)
    list = []
    list.append(item)
    list.append(item)
    a = ['name', 'address', 'price', 'comment']
    with open('mycsvfile.csv', 'a+', encoding='GBK', newline="") as f:
        w = csv.DictWriter(f, a)
        w.writeheader()
        for li in list:
            w.writerow(li)
        f.close()