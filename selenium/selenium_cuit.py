# @File  : selenium_cuit.py
# @Author: Park boy
# @Date  : 2021-08-03
import time
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from word_chioce import process_item
from bs4 import BeautifulSoup
# from lxml import etree


def sign_dazong():
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://account.dianping.com/login?redir=https://www.dianping.com')
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    choices = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]')
    choices.click()
    time.sleep(0.5)
    choices2 = driver.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div[1]/span[2]')
    choices2.click()
    time.sleep(0.5)
    num = driver.find_element_by_xpath('//*[@id="account-textbox"]')
    num.send_keys('13882363117')
    time.sleep(0.5)
    passwd = driver.find_element_by_xpath('//*[@id="password-textbox"]')
    passwd.send_keys('zxc159123')
    time.sleep(0.5)
    click = driver.find_element_by_xpath('//*[@id="login-button-account"]')
    click.click()
    time.sleep(16)
    return driver


def choice_tea(driver):
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')   # 接管打开浏览器，避免被检测出来
    driver = webdriver.Chrome(chrome_options=chrome_options)
    item = {}
    page_list = []
    driver.get('http://www.dianping.com/shuangliu/ch30/g134p50')
    time.sleep(0.5)
    page_list.append(driver.page_source)
    for i in range(6):
        next_page = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/a[@class="next"]')
        next_page.click()
        time.sleep(1)
        page_list.append(driver.page_source)
    for page_1 in page_list:
        soup = BeautifulSoup(page_1, 'lxml')
        text = soup.find(id='shop-all-list')
        text = text.find_all(name='li')
        for info in text:
            name = info.find(name='h4').text
            if len(info.find_all(name='b')) == 1:
                comment = info.find_all(name='b')[0].text
                price = None
            elif len(info.find_all(name='b')) == 2:
                comment = info.find_all(name='b')[0].text
                price = info.find_all(name='b')[1].text
            else:
                comment = None
                price = None
            address = info.find(name='div', class_='tag-addr').text.split('\n')
            item['name'] = name
            item['comment'] = comment
            item['price'] = price
            item['address'] = "".join(address)
            time.sleep(0.5)
            save_csv(item)


def save_csv(items):
    items = process_item(items)
    a = ['name', 'address', 'price', 'comment']
    with open('dazong.csv', 'a+', encoding='GBK', newline="") as f:
        w = csv.DictWriter(f, a)
        w.writerow(items)
        f.close()


if __name__ == '__main__':
    # driver = sign_dazong()
    # a = ['name', 'address', 'price', 'comment']
    # with open('dazong.csv', 'a+', encoding='GBK', newline="") as f:
    #     w = csv.DictWriter(f, a)
    #     w.writeheader()
    #     f.close()
    choice_tea(1)

