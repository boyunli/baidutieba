# coding:utf-8

import time
import json
import re
import pprint

import requests
from selenium import webdriver

from settings import mouse_crack, VCODE_DIC, HEADERS


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
        driver.get(self.base_url)
        print("start login")
        chg_field = driver.find_element_by_class_name("u_login").find_element_by_class_name("u_menu_item")
        chg_field.click()
        
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
        print "login cookies: "
        pprint.pprint(login_cookies)
        return login_cookies    

    def post_data(self, data=None):
        url_post = "https://tieba.baidu.com/f/commit/thread/add"
        tbs = self._get_tbs()
        timestamp = str(int(time.time()*1000))
        print 'tbs: '+ tbs
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
        print "verify post cookies: "
        pprint.pprint(self.session.cookies.get_dict())
        res_text = res.json()
        # import pdb
        # pdb.set_trace()
        if res_text['err_code'] == 0:
            tid = res_text['data']['tid']   #帖子ID
            print "post success, tid is {}".format(tid)
        # 当出现要输入验证码
        elif res_text['err_code'] == 40:
            print "Need input verification code!!!"
            vcode_md5 = res_text['data']['vcode']["captcha_vcode_str"]
            data['vcode_md5'] = vcode_md5
            vcode_url = 'https://tieba.baidu.com/cgi-bin/genimg?'+vcode_md5
            vcode_req = requests.get(vcode_url, headers=HEADERS, verify=False)
            # download the vcode img
            with open('../static/images/vcode_{}.jpg'\
                    .format(datetime.datetime.now().strftime('%Y_%m_%d_%H_%m')),
                 'wb') as out:
                out.write(vcode_req.content)
                out.flush()
            #先手动输入vcode
            vcode_num = raw_input(u'input vcode:')
            vcode = ''
            for i in str(vcode_num):
                vcode += VCODE_DIC[i]
            print 'vcode: ' + vcode
            data['vcode'] = vcode
            self.post_data(data)
            # import pdb
            # pdb.set_trace()
        else:
            with open('log/error_code.txt','a') as out:
                out.write('*'*30 + str(datetime.datetime.now()))
                out.write('\n')
                out.write('百度贴吧error_code值: '+str(res_text['err_code']))
                out.write('\n')
            print "post data failed"       
        return res_text


if __name__ == "__main__":
    login_name = raw_input("please input username:\n")
    login_passwd = raw_input("please input password:\n")
    post = Post(login_name, login_passwd)
