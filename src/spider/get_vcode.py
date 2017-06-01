# coding:utf-8

import time
import datetime
import json
import random
import threading

TOTAL = 0

import requests

from settings import HEADERS

'''
该脚本只为获取vcode图片,做ocr训练集用
'''

def get_cookies():
    with open("../../cookies/login_cookies.json") as f:
            cookies = json.load(f)


class GetVcode(threading.Thread):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.cookies = get_cookies()
        super(GetVcode, self).__init__(*args, **kwargs)
        
    def run(self):
        global TOTAL
        for i in xrange(3):
            # import pdb
            # pdb.set_trace()
            resp = requests.get(self.url, headers=HEADERS, verify=False, cookies=self.cookies)
            with open('../ocr/images/vcode/vcode_{}.png'\
                            .format(random.randint(0, 10000)),
                        'wb') as out:
                out.write(resp.content)
                out.flush()
                time.sleep(5)
            TOTAL += 1
            print 'total:{} '.format(TOTAL)

if __name__ == '__main__':
    vcode_urls = [
        'https://tieba.baidu.com/cgi-bin/genimg?captchaservice636533315172544b704864682f5854556b6b767168496533656c347469304c66624374617935345336396857724b4477776f5734317456723731612b326c72566b635644796e346e475a7542584a516e3162646368554437355343566364325655767136336b35634f786a796a546d3141627964715639325872774374466a7942725079536d634473307a646a457737484973717a5439787335427a354c67747a32536e514b6f39783253684772374b57654a67733955463632446d55613758303563754a4f574f4e48355948634975445133426155424d6f2b692f37552f514135586c566573714641434f50786a314e54796759424a38594b4d3233723558343368593375397057717856426550716650445a69316b73687a6f31415864797a434459684f7145416b54392b69695349653769',
        'https://tieba.baidu.com/cgi-bin/genimg?captchaservice653733346b687741755162355567613233595671592f696a724b7a2b7a7676327672766878674a4c2b4162377447435051794c6d59725a78536677474f5a5146665335783179615555654d4f47527963514a4b344c626972426a4d6f5178534756367667472f595477437554774348754c6346713451773478316f6f68794c484e694c337174423936594b54364c506d4d6f7055366f31357a59434261587475676954337367346a45786e636165663466786d79445442536c6a7a4a70522f6d36797439324d657464516d45304d4e4d554750585a384d6562724648514e446e38696e7266665461306a6c2f4c46555242624b5777495a53307276323268694d4550666468797841354776754877364978336d594131654d587870694643444f765633376b74646e536f2f6947346976537930',
    ]
    try:
        for url in vcode_urls:
            a = GetVcode(url)
            b = GetVcode(url)
            c = GetVcode(url)
            a.start()
            b.start()
            c.start()
    except Exception as e:
        print e