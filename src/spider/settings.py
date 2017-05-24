# -*- coding: utf8 -*-

import os

URL_BAIDU_INDEX = u'http://www.baidu.com/'

#login urls. Here use tpl=pp to get token value. This will allow
URL_BAIDU_TOKEN = 'https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&class=login'
URL_BAIDU_LOGIN = 'https://passport.baidu.com/v2/api/?login'

#检测是否登陆成功
INFO_BAIDU      = 'http://i.baidu.com/'

#发帖对应的链接
ADD_THREAD = 'http://tieba.baidu.com/f/commit/thread/add'

#GET验证码的链接
VCODE_IMAGE = 'http://tieba.baidu.com/cgi-bin/genimg?'

#生成贴吧连接
TIEBA_BASEURL = 'http://tieba.baidu.com'

#贴吧搜索链接
search_URL = 'http://tieba.baidu.com/f/search/fm?'

#设置账号密码的部分
username = ''    #用户名
password = ''    #密码



#用来构建发帖数据的真实mouse_pwd
mouse_crack = [
        '55,61,61,41,49,48,52,53,12,52,41,53,41,52,41,53,41,52,41,53,12,49,55,53,49,60,61,51,12,52,55,61,53,41,61,53,53,',
        '119,114,124,105,113,115,114,115,76,116,105,117,105,116,105,117,105,116,105,117,105,116,105,117,105,116,105,117,76,112,117,115,125,114,117,112,76,116,119,125,117,105,125,117,117,',
        '57,56,58,38,62,63,56,57,3,59,38,58,38,59,38,58,38,59,38,58,38,59,38,58,38,59,38,58,3,59,60,61,63,57,61,3,59,56,50,58,38,50,58,58,',
        '11,11,15,20,12,11,9,0,49,9,20,8,20,9,20,8,20,9,20,8,20,9,20,8,20,9,20,8,49,13,11,11,9,13,49,9,10,0,8,20,0,8,8,',
        '16,21,20,8,16,17,22,29,45,21,8,20,8,21,8,20,8,21,8,20,45,17,23,23,19,23,45,21,22,28,20,8,28,20,20,',
        '5,14,0,27,3,4,6,4,62,6,27,7,27,6,27,7,27,6,27,7,27,6,27,7,27,6,27,7,62,6,5,6,1,7,14,3,62,6,5,15,7,27,15,7,7,',
        '7,28,25,4,28,29,24,30,33,25,4,24,4,25,4,24,4,25,4,24,4,25,4,24,4,25,4,24,33,28,16,27,29,24,33,25,26,16,24,4,16,24,24,',
        '58,56,48,37,61,60,59,57,0,56,37,57,37,56,37,57,37,56,37,57,37,56,37,57,37,56,37,57,0,63,59,63,60,57,0,56,59,49,57,37,49,57,57,',
        '112,113,115,111,119,118,113,112,74,114,111,115,111,114,111,115,111,114,111,115,111,114,111,115,111,114,111,115,74,117,119,122,116,117,74,114,113,123,115,111,123,115,115,',
        '17,21,29,9,17,16,23,17,44,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,44,17,17,29,29,16,44,20,23,29,21,9,29,21,21,'
        '17,21,29,9,17,16,23,17,44,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,9,20,9,21,44,17,17,29,29,16,44,20,23,29,21,9,29,21,21,',
    ]


#对应的验证码九宫格的坐标，用于生成验证码序列
VCODE_DIC = {
    '1' :   '00000000',
    '2' :   '00010000',
    '3' :   '00020000',
    '4' :   '00000001',
    '5' :   '00010001',
    '6' :   '00020001',
    '7' :   '00000002',
    '8' :   '00010002',
    '9' :   '00020002'
}


HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept-encoding": "gzip",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(pathname)s:%(lineno)d][%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    #过滤器，表明一个日志信息是否要被过滤掉而不记录
    'filters': {                                         
    },
    #处理器
    'handlers': {
        'spider': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/spider.log',
            'maxBytes': 1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
        },
        'spider_error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/spider_error.log',
            'maxBytes':1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'ocr': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':BASE_DIR + '/log/ocr.log',
            'maxBytes': 1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'ocr_error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/ocr_error.log',
            'maxBytes':1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
    },
    # 记录器
    'loggers': {
        'myocr': {
            'handlers': ['console', 'ocr', 'ocr_error'],
            'level': 'DEBUG',  #级别最低
            'propagate': True
        },
        'myspider': {
            'handlers': ['console', 'spider', 'spider_error'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}