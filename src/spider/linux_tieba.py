# coding:utf-8
'''
1、利用 selenium +phantomjs(Linuxs字符终端下) 模拟登录，获得登录cookies(已获得)
2、再跟踪从登录到发文的过程中cookie的变化情况，拿到最终cookies(成功)
3、如果跳过第2步（已注释的代码实现了其功能），直接以login_cookies能发文成功，则跳过第2步
'''

import time
import json
import re
import os
import pprint
import datetime
import random
import logging
import logging.config

import requests
from selenium import webdriver

from settings import mouse_crack, VCODE_DIC, HEADERS, LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('myspider')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  

class BaiduPoster(object):
    def __init__(self, username, password):
        self.base_url =  "http://tieba.baidu.com/f?kw=临高房产&ie=utf-8"
        self.username = username
        self.password = password
        self.session = requests.Session()  
        try:
            self._get_cookies()
        except IOError as e:
            logger.error(e)
        if self._check_login():            
            logger.debug('from cache cookies:{}'.format(pprint.pformat(self.session.cookies)))
            self.post_data()
        else:
            # 防止cookie过期失效
            self.session.cookies.clear()
            self._login()
            self.post_data()

    def _check_login(self, page_html=None):
        res = self.session.get(self.base_url, headers=HEADERS, verify=False)
        if page_html:
            text = page_html
            test_key = "个人中心".decode("utf-8")
            login_key = re.search(test_key, text)      
        else:
            text = res.text
            login_key = int(re.findall(r"'is_login':\s?(\d)", text)[0])
        if login_key:
            return True
        else:
            return False

    def _get_cookies(self):
        """从文本中获得cookie
        """
        cookie_file = os.path.join(BASE_DIR, "cookies/login_cookies.json" )
        with open(cookie_file) as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)

    def _login(self):
        # import pdb
        # pdb.set_trace()
        driver = webdriver.PhantomJS()
        driver.get(self.base_url)
        logger.debug("start login")
        chg_field = driver.find_element_by_class_name("u_login").find_element_by_class_name("u_menu_item")
        chg_field.click()
        
        time.sleep(20)  #等页面加载完
        username_field = driver.find_element_by_id("TANGRAM__PSP_9__userName")   
        try:
            username_field.send_keys(self.username)
        except Exception as e:
            username_field.send_keys(self.username.decode("utf-8"))    #当用户名是以中文形式
        passwd_field = driver.find_element_by_id("TANGRAM__PSP_9__password")
        passwd_field.send_keys(self.password)
        login_button = driver.find_element_by_id("TANGRAM__PSP_9__submit")
        login_button.click()
        time.sleep(20)

        cookies = driver.get_cookies()
        login_cookies = {item["name"] : item["value"] for item in cookies}     
        page_html = driver.page_source
        if self._check_login(page_html):
            with open("../cookies/login_cookies.json", "w") as f:
                json.dump(login_cookies, f)     
            self.session.cookies.update(login_cookies)
            logger.debug('login success')
        else:
            logger.debug('login failed')
        logger.debug('login cookies: {} '.format(pprint.pformat(login_cookies)))
        return login_cookies    
    
    def _get_tbs(self):
        url_tbs = "http://tieba.baidu.com/dc/common/tbs"
        return self.session.get(url_tbs, headers=HEADERS).json()["tbs"]

    def post_data(self, data=None):
        url_post = "https://tieba.baidu.com/f/commit/thread/add"
        tbs = self._get_tbs()
        timestamp = str(int(time.time()*1000))
        logger.debug('tbs: {}'.format(tbs)) 
        if data is None:
            data={
                "ie":"utf-8", 
                "kw":"临高房产",      # 根据贴吧主题
                "fid":"15820065",    # 根据贴吧主题
                "tid":0, 
                "floor_num": 0, 
                "rich_text": 1, 
                "basilisk":1,
                "mouse_pwd_isclick":0,
                "__type__": "thread",
            
                "content": "海南万宁中信泰富神州半岛",      
                "title":"海南万宁中信泰富神州半岛", 
                "mouse_pwd_t": timestamp,
                'mouse_pwd' :  mouse_crack[random.randint(0, len(mouse_crack)) - 1] + timestamp,

                "tbs": tbs,   #change
                "vcode_md5": '',   #change
                }
        else:
            data = data

        res = self.session.post(url_post, data=data, headers=HEADERS, verify=False)
        logger.debug("verify post cookies: {}".format(pprint.pformat(self.session.cookies.get_dict())))
        res_text = res.json()
        # import pdb
        # pdb.set_trace()
        if res_text['err_code'] == 0:
            tid = res_text['data']['tid']   #帖子ID
            logger.debug("post success, tid is {}".format(tid))
        # 当出现要输入验证码
        elif res_text['err_code'] == 40:
            logger.debug("Need input verification code!!!")
            vcode_md5 = res_text['data']['vcode']["captcha_vcode_str"]
            data['vcode_md5'] = vcode_md5
            vcode_url = 'https://tieba.baidu.com/cgi-bin/genimg?'+vcode_md5
            with open('../log/vcode_url.txt', 'a') as f:
                f.write(vcode_url)
            vcode_req = requests.get(vcode_url, headers=HEADERS, verify=False)
            # download the vcode img, 注意验证码图片保存格式为.png， 
            with open('../static/images/vcode_{}.png'\
                    .format(datetime.datetime.now().strftime('%Y_%m_%d_%H_%m')),
                 'wb') as out:
                out.write(vcode_req.content)
                out.flush()
            #先手动输入vcode
            vcode_num = raw_input(u'input vcode:')
            vcode = ''
            for i in str(vcode_num):
                vcode += VCODE_DIC[i]
            logger.debug('vcode: {}'.format(vcode))
            data['vcode'] = vcode
            self.post_data(data)
        else:
            with open('log/error_code.txt','a') as out:
                out.write('*'*30 + str(datetime.datetime.now()))
                out.write('\n')
                out.write('百度贴吧error_code值: '+str(res_text['err_code']))
                out.write('\n')
            logger.debug("post data failed")
        return res_text


if __name__ == "__main__":
    # login_name = raw_input("please input username:\n")
    # login_passwd = raw_input("please input password:\n")
    username =  "狮子零零蛋123"
    password = "19910414ll"
    post = BaiduPoster(username, password)
    
     