# @File  : test.py
# @Author: Park boy
# @Date  : 2021-08-01
from fontTools.ttLib import TTFont
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'Host': 'wreport2.meituan.net',
    'Referer': 'http://www.dianping.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62 ',
    # 'cookie': 'fspop=test; _lx_utm=utm_source=Baidu&utm_medium=organic; '
    #           '_lxsdk_cuid=17b017f8affc8-06f71231a8e514-7e687969-144000-17b017f8affc8; '
    #           '_lxsdk=17b017f8affc8-06f71231a8e514-7e687969-144000-17b017f8affc8; '
    #           '_hc.v=f1a52a49-f5c1-8e03-1ea2-703a8b2a5c76.1627817741; '
    #           'Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1627817742; s_ViewType=10; cy=8; cye=chengdu; '
    #           'dplet=f41712409e1a22c1b9e5d3da8e2dc874; '
    #           'dper=afd4096b02e3d4e0819657b39b2b4057cdfc944dba5738267bc7b772787d7d1fb634ebd61c54f15ae5172e62e48aa85a1ebfe5a2d3b771e1e03fc1a11b96e5f0d3625dcd3748dba23ee5032c4dd0ff2dbb8830284ae2677b4d124ca79e515764; ua=bo_y; ctu=49c636057a583d1f092f0432f113a3cb01624eaab69e8861a3a88c17130e5752; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=17b0457671b-752-0b8-7d1||NaN',
}

woff_str_601 = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺' \
               '花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西' \
               '批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居' \
               '庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川' \
               '泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙' \
               '恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下臬凤港开关景泉' \
               '塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦' \
               '字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位' \
               '能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置' \
               '适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'


def process_item(item):
    address = item['address']
    price = item['price']
    comment = item['comment']
    item['address'] = unicode_item(address)
    item['price'] = unicode_item(price)
    item['comment'] = unicode_item(comment)
    return item


def unicode_item(info):
    info = repr(info).replace(r'\u', 'uni')
    if 'tagName' in info:
        return info_name('tagName', info)
    elif 'shopNum' in info:
        return info_name('shopNum', info)


def info_name(adds, info):
    font = TTFont('./' + adds + '.woff')
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


from_data = {
    'countrycode': '86',
    'username': '13882363117',
    'keepLogin': 'on',
    'encryptPassword': 'WJISdMOiaZmwDbQz3wY1teK/1e/E4DHd4wGdccZ6meoVPpXRSwWyrYvfGKa1/zjmG3IoFK6a/UbQlBRf/E3AvWrQsiJLqv++0sFCn64Tl617or3aIUxnrKt4QKyJQU3DFx2npRpC8echZS9Kkpu30BOffUE7AB0B2q8Gw+S9fP4=',
    '_token': 'eJx9k2tvokAUhv8LSfulRGYYZgATswEV67UW0VS7TYOAguUmUFE3+993oHW2ZjdN5sNzbu+5JPOLy/ou1+QgAEBSOZ47eFllNkCDUKvIuSYkoqwCCWAEiMhzzhcfVBDGKs+ts0WHaz6LKuCRjF8qh0ntZ4gR4RUivfCfCMkLL0r0VTl9msL5RZHmTUGwHSd5j4uGG9hxGsTbhpNEF6cQbDI78kbJNoh/OHYYrm3nrdW181Pteq2jr5cAuC0D12tt7DD3btMsKRInCVsffW4zzw2yD+MGaTeiQV9Zlldt6d7fThXWc3xRoon/aNAFI6taEBKZh1imopCoV1QdGMqAEWSErgjXJFKSGCFWITIVkSl/kMJIZkQutQRf9IjEiHUjkBG4EFYZKYxkRuSK6ukxviL5W1Kqk73VJ/uZ8f3JdG7RmMNozchmFDDy/hNtM3pitPok2suuewEe8Prcsh4mf2di2VCl+wHMbBEpPBZ5rU5FPEKIn021SaVWVGqV6ph+HxrPg21MyRuURumEp+1O07SJvllax9I3tUjq9zonY9i/X4TDvVuW/mC5nz0eR8ehgA4m8tv4EJqxfz81N2mo93BghVkKwqP4FMIotVyMwiSCXQMKpQEfn8aG/q719l13cz8Tg13R7u3MmZCKg5gM5upsebCPws7wg4Nw7vXaS6W0E7SPCkFNdm7bM/wsmqsdL97nUbR6AKuuf3f3/rAdj8P1YLo/zWaebB4P9kLW+/epbelWQIzRCWJT3ujj0WQKzwh6viPoE4T2Uu6OhpuVsIpjslsMzpKsaMr5YIZJOoR9Ya65Bhj1t4GWo7zjqel08Nhqcb//AAeMPaM='

}
if __name__ == '__main__':
    session = requests.Session()
    url = 'https://account.dianping.com/account/ajax/passwordLogin'
    url2 = 'http://www.dianping.com/chengdu/ch30/g134p2'
    response = session.post(url, headers=headers)
    print(response.text)
    response2 = session.get(url2, headers=headers)
    # print(response2.text)
