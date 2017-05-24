# -*- coding:utf-8 -*-

import time

import requests

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
        self.base_url = 'http://tieba.baidu.com/f?kw=海口房产&ie=utf-8'
        self.session = requests.Session()

    def _get_curtime(self):
        return int(time.time()*1000)
    
    def get_token(gid, callback):
        cur_time = _get_curtime()
        get_data = {
            'tpl': 'netdisk',
            'subpro': 'netdisk_web',
            'apiver': 'v3',
            'tt': cur_time,
            'class': 'login',
            'gid': gid,
            'logintype': 'basicLogin',
            'callback': callback
        }
        headers.update(dict(Referer='http://pan.baidu.com/', Accept='*/*', Connection='keep-alive', Host='passport.baidu.com'))
        resp = session.get(url='https://passport.baidu.com/v2/api/?getapi', params=get_data, headers=headers)
        if resp.status_code == 200 and callback in resp.text:
            # 如果json字符串中带有单引号，会解析出错，只有统一成双引号才可以正确的解析
            #data = eval(re.search(r'.*?\((.*)\)', resp.text).group(1))
            data = json.loads(re.search(r'.*?\((.*)\)', resp.text).group(1).replace("'", '"'))
            return data.get('data').get('token')
        else:
            print('获取token失败')
            return None



if __name__ == "__main__":
    # login_name = raw_input("please input username:\n")
    # login_passwd = raw_input("please input password:\n")
    username =  "猫笑的甜蜜蜜"
    password = "515550ll"
    post = Post(username, password)
 