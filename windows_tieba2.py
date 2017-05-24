# coding:utf-8
'''
利用selenium模拟登录和模拟发文一次， 获得发文的cookies；(此时要想实现第一次发文，可能会要求输入验证码)
后续发文都用 最后的cookies， 采用requests 伪装登录状态，并post数据到百度服务器；

成功
'''


import time
import json
import re
import pprint

import requests
from selenium import webdriver

HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept-encoding": "gzip",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }


class Post(object):
    def __init__(self, username, password):
        self.session = requests.Session()
        self.void_verify(username, password)
        try:
            self._get_cookies()
        except IOError as e:
            print e
        self.post_message_again()


    def _get_cookies(self):
        """从文本中获得cookie
        """
        with open("cookies/post_cookies.json") as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)
    

    def _login(self, name, passwd):
        url = "http://tieba.baidu.com/f?kw=海口房产&ie=utf-8"
        # 这里可以用Chrome、Phantomjs等，如果没有加入环境变量，需要指定具体的位置
        driver = webdriver.Chrome(executable_path="C:/Program Files (x86)/Google/Chrome/Application/chromedriver")
        driver.maximize_window()
        driver.get(url)
        print("start login")
        chg_field = driver.find_element_by_class_name("u_login").find_element_by_class_name("u_menu_item")
        chg_field.click()
        # import pdb
        # pdb.set_trace()
        time.sleep(20)  #等页面加载完
        name_field = driver.find_element_by_id("TANGRAM__PSP_9__userName")
    
        try:
            name_field.send_keys(name)
        except Exception as e:
            name_field.send_keys(name.decode("utf-8"))    #当用户名是以中文形式
        passwd_field = driver.find_element_by_id("TANGRAM__PSP_9__password")
        passwd_field.send_keys(passwd)
        login_button = driver.find_element_by_id("TANGRAM__PSP_9__submit")
        login_button.click()
        time.sleep(20)
        cookies = driver.get_cookies()
        cookies = {item["name"] : item["value"] for item in cookies}
        
        page_html = driver.page_source
        test_key = "个人中心".decode("utf-8")
        if test_key in page_html:
            with open("cookies/login_cookies.json", "w") as f:
                json.dump(cookies, f)
            print 'login success'
        else:
            print 'login failed'
        return driver

    def post_message(self, driver):
        # input_title = driver.find_element_by_class_name("j_title_wrap").find_element_by_class_name("editor_textfield editor_title ui_textfield j_title j_topic_sug_input normal-prefix")
        title = 'haikou housing price'
        input_title = driver.find_element_by_class_name("j_title_wrap").find_element_by_class_name("editor_textfield")
        input_title.send_keys(title)
        input_content = driver.find_element_by_class_name("edui-editor-middle").find_element_by_id("ueditor_replace")
        input_content.send_keys('will increase?')
        # submit_button = driver.find_element_by_class("btn_default btn_middle j_submit poster_submit")
        submit_button = driver.find_element_by_class_name("poster_submit")
        submit_button.click()
        time.sleep(20)

        page_html = driver.page_source
        if title in page_html:
            print "posts success"
        else:
            print "posts failed"

        cookies = driver.get_cookies()
        cookies = {item["name"] : item["value"] for item in cookies}
        print 'post cookies: '
        pprint.pprint(cookies)
        with open("cookies/post_cookies.json", "w") as f:
                json.dump(cookies, f)
        return cookies
    
    def change_again_cookies(self, username, password):
        cookies = self.post_message(self._login(username, password))
        change_cookies_url = 'https://tbmsg.baidu.com/gmessage/get?mtype=1&_={}'.format(int(time.time()*1000))
        change_again_cookies = requests.get(change_cookies_url, headers=HEADERS, cookies=cookies, verify=False).cookies
        print 'change_again_cookies: '
        pprint.pprint(change_again_cookies)
        change_again_cookies = {item["name"] : item["value"] for item in change_again_cookies}
        post_cookies = cookies.update(change_again_cookies)
        with open("cookies/post_again_cookies.json", "w") as f:
                json.dump(post_cookies, f)
        return post_cookies
    
    def void_verify(self, username, password):
        post_cookies = self.change_again_cookies(username, password)
        verify_url = "http://tieba.baidu.com/messagepool/listen?user=6046c3a8d0a6b5c4ccf0c3dbc3db33b6&c=10_1495419693972&v={}".format(int(time.time()*1000))
        verify = requests.get(verify_url, headers=HEADERS, cookies=post_cookies, verify=False)
        return verify


    def _get_tbs(self):
        url_tbs = "http://tieba.baidu.com/dc/common/tbs"
        return self.session.get(url_tbs, headers=HEADERS).json()["tbs"]

    def post_message_again(self):
        url_post = "https://tieba.baidu.com/f/commit/thread/add"
        tbs = self._get_tbs()
        print 'tbs: '+ tbs
        data={
            "ie":"utf-8", 
            "kw":"海口房产", 
            "fid":"1097712", 
            "tid":0, 
            "floor_num": 0, 
            "rich_text": 1, 
            "basilisk":1,
            "mouse_pwd_isclick":0,
            "__type__": "thread",
        
            "content": "海口哪里环境好",      
            "title":"听说气候适宜", 
            "mouse_pwd_t": int(time.time()*1000),

            "tbs": tbs,   #change
            "vcode_md5": '',   #change
            }
        print "post message again cookies: "
        pprint.pprint(self.session.cookies.get_dict())
        res = self.session.post(url_post, data=data, headers=HEADERS, verify=False)
        # import pdb
        # pdb.set_trace()
        return res


if __name__ == "__main__":
    # login_name = raw_input("please input username:\n")
    # login_passwd = raw_input("please input password:\n")
    login_name =  "猫笑的甜蜜蜜"
    login_passwd = "515550ll"
    post = Post(login_name, login_passwd)

     