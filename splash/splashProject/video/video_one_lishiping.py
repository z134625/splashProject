# @File  : video_one_lishiping.py
# @Author: Park boy
# @Date  : 2021-07-31
import requests
import re

response = requests.get('https://pic.netbian.com/4kmeinv/')
response.encoding = 'gbk'
res = re.findall('<li>.*?img src="(.*?)" alt=.*?<b>(.*?)</b>.*?', response.text, re.S)
for i in res:
    print(i)
