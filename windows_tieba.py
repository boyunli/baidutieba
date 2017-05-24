# coding:utf-8
'''
1、利用 selenium +chrome(windows下) 模拟登录，获得登录cookies(已获得)
2、再跟踪从登录到发文的过程中cookie的变化情况，拿到最终cookies(成功)
3、如果跳过第2步（已注释的代码实现了其功能），直接以login_cookies能发文成功，则跳过第2步
表示面对需要输入验证码的情况，暂时未解决。
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
        self.base_url =  "http://tieba.baidu.com/f?kw=海口房产&ie=utf-8"
        self.session = requests.Session()  
        # self.change_again_cookies(username, password)
        self._login(username, password)
        # import pdb
        # pdb.set_trace()
        try:
            self._get_cookies()
        except IOError as e:
            print e
        if self._check_login():            
            print 'from cache...cookies...'
            pprint.pprint(self.session.cookies)    
            self.post_message()
        else:
            # 防止cookie过期失效
            self.session.cookies.clear()
            self._login(username, password)
            self.post_message()

    def _check_login(self, page_html=None):
        """验证是否登陆成功
        Returns:
            Boolean: 是否登陆成功
        """
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

    def _get_tbs(self):
        url_tbs = "http://tieba.baidu.com/dc/common/tbs"
        return self.session.get(url_tbs, headers=HEADERS).json()["tbs"]

    def _get_cookies(self):
        """从文本中获得cookie
        """
        with open("cookies/login_cookies.json") as f:
            cookies = json.load(f)
            self.session.cookies.update(cookies)

    def _login(self, username, password):
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
        username_field = driver.find_element_by_id("TANGRAM__PSP_9__userName")
    
        try:
            username_field.send_keys(username)
        except Exception as e:
            username_field.send_keys(username.decode("utf-8"))    #当用户名是以中文形式
        passwd_field = driver.find_element_by_id("TANGRAM__PSP_9__password")
        passwd_field.send_keys(password)
        login_button = driver.find_element_by_id("TANGRAM__PSP_9__submit")
        login_button.click()
        time.sleep(20)

        cookies = driver.get_cookies()
        login_cookies = {item["name"] : item["value"] for item in cookies}     
        page_html = driver.page_source
        if self._check_login(page_html):
            with open("cookies/login_cookies.json", "w") as f:
                json.dump(login_cookies, f)     
            self.session.cookies.update(login_cookies)
            print 'login success'
        else:
            print 'login failed'
        return login_cookies

    # # 在登录和提交贴文之间，cookie值还经历了两次变化：
    # def change_cookies(self, username, password):
    #     login_cookies = self._login(username, password)
    #     change_cookies_url = 'https://tieba.baidu.com/f/user/sign_list?t={}'.format(int(time.time()*1000))
    #     # import pdb
    #     # pdb.set_trace()
    #     change_cookies = requests.get(change_cookies_url, headers=HEADERS, cookies=login_cookies, verify=False).cookies
    #     print 'change_cookies: '
    #     pprint.pprint(change_cookies)
    #     change_cookies = {item["name"] : item["value"] for item in change_cookies.get_dict()}
    #     cookies = login_cookies.update(change_cookies)
    #     return cookies

    # # 在登录和提交贴文之间，cookie值还经历了两次变化：
    # def change_again_cookies(self, username, password):
    #     cookies = self.change_cookies(username, password)
    #     change_cookies_url = 'https://tbmsg.baidu.com/gmessage/get?mtype=1&_={}'.format(int(time.time()*1000))
    #     change_again_cookies = requests.get(change_cookies_url, headers=HEADERS, cookies=cookies, verify=False).cookies
    #     print 'change_again_cookies: '
    #     pprint.pprint(change_again_cookies)
    #     change_again_cookies = {item["name"] : item["value"] for item in change_again_cookies.get_dict()}
    #     post_cookies = cookies.update(change_again_cookies)
    #     with open("cookies/post_cookies.json", "w") as f:
    #             json.dump(post_cookies, f)
    #     return post_cookies
    

    def post_message(self):
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
        
            "content": "海南琼海碧桂园东海岸小区",      
            "title":"海南琼海碧桂园东海岸小区", 
            "mouse_pwd_t": int(time.time()*1000),

            "tbs": tbs,   #change
            "vcode_md5": '',   #change
            }
        print "verify post cookies: "
        pprint.pprint(self.session.cookies.get_dict())
        res = self.session.post(url_post, data=data, headers=HEADERS, verify=False)
        # import pdb
        # pdb.set_trace()
        if res.json()['err_code'] == 0:
            tid = res.json()['tid']   #帖子ID
            print "post success, tid is {}".format(tid)
        # 当出现要输入验证码
        elif res.json()['err_code'] == 40:
            # import pdb
            # pdb.set_trace()
            print "Need input verification code!!!"
            print "post failed"
        return res.json()

if __name__ == "__main__":
    # login_name = raw_input("please input username:\n")
    # login_passwd = raw_input("please input password:\n")
    login_name =  "猫笑的甜蜜蜜"
    login_passwd = "515550ll"
    post = Post(login_name, login_passwd)