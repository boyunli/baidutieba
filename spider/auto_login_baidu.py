# coding:utf-8

import time
import json

import requests
from selenium import webdriver

HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Accept-encoding': 'gzip',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            }

def login(name, passwd):
    url = 'http://tieba.baidu.com/f?kw=广州房产&ie=utf-8'
    # 这里可以用Chrome、Phantomjs等，如果没有加入环境变量，需要指定具体的位置
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver')
    driver.maximize_window()
    driver.get(url)
    print('start login')
    chg_field = driver.find_element_by_class_name('u_login').find_element_by_class_name('u_menu_item')
    chg_field.click()
    time.sleep(10)  #等页面加载完
    name_field = driver.find_element_by_id('TANGRAM__PSP_9__userName')
  
    try:
        name_field.send_keys(name)
    except Exception as e:
        name_field.send_keys(name.decode('utf-8'))    #当用户名是以中文形式
    passwd_field = driver.find_element_by_id('TANGRAM__PSP_9__password')
    passwd_field.send_keys(passwd)
    login_button = driver.find_element_by_id('TANGRAM__PSP_9__submit')
    login_button.click()
    time.sleep(20)
    # import pdb
    # pdb.set_trace()
    cookies = driver.get_cookies()
    with open('cookie.json', 'w') as f:
            json.dump(cookies, f)
    import pdb
    pdb.set_trace()
    return cookies


if __name__ == '__main__':
    # login_name = raw_input('please input username:\n')
    # login_passwd = raw_input('please input password:\n')
    login_name =  '猫笑的甜蜜蜜'
    login_passwd = '515550ll'
    cookies = login(login_name, login_passwd)
    print cookies