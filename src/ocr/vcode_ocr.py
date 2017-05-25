# -*- coding: utf_8 -*-
'''
  验证码为透明底，黑字
  一、预处理阶段
    1、灰度化，二值化，去噪， 去干扰线
    2、对1处理后的图片分割切图
    3、图片尺寸归一化：分割后的单字标准化为32*32像素大小
  二、
    图片字符标记
    字符图片特征提取
    生成特征和标记对应的训练数据集
    训练特征标记数据生成识别模型
    使用识别模型预测新的未知图片集
    达到根据“图片”就能返回识别正确的字符集的目标
'''

import os
import sys
import logging
import logging.config

import cv2
import numpy as np
# from matplotlib import pyplot as plt
from PIL import Image,ImageEnhance,ImageFilter

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from spider.settings import LOGGING
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('myocr')

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ORIGINDIR = os.path.join(BASEDIR, 'images/origin/')
RGBADIR = os.path.join(BASEDIR, 'images/rgba/')

VCODEDIR = os.path.join(BASEDIR, 'images/vcode/')
CORR_VCODEDIR = os.path.join(BASEDIR, 'images/corr_vcode/')

class PreProcess(object):

    def trans_la_to_rgba(self, origin_img, filename):
        '''
        将透明底色变成白底(即图片mode从LA 转换成 RGBA)
        '''
        rgba_path = os.path.join(RGBADIR, filename)
        logger.debug('rgba_path: {}'.format(rgba_path))
        width, height = origin_img.size 
        im_rgba = origin_img.convert('RGBA')      
        new_rgba = Image.new('RGBA', im_rgba.size, 'white') 
        new_rgba.paste(im_rgba, (0, 0, width, height), im_rgba)
        new_rgba.save(rgba_path)
        return new_rgba
    
    def cut_two_pics(self, pic, filename):
        '''
        分离验证码和九宫图中的汉字
        '''
        vcode_path = os.path.join(VCODEDIR, filename)
        corr_path = os.path.join(CORR_VCODEDIR, filename)
        vcode_box = (0, 0, 240, 85)
        corr_box = (0, 86, 240, 320)
        vcode_region = pic.crop(vcode_box)
        corr_region = pic.crop(corr_box)
        vcode_region.save(vcode_path)
        corr_region.save(corr_path)
        return vcode_region

    

if __name__ == '__main__':
    origin_imgs = os.listdir(ORIGINDIR)
    pp = PreProcess()
    for filename in origin_imgs:
        origin_path = os.path.join(ORIGINDIR, filename)
        img = Image.open(origin_path)
        new_rgba = pp.trans_la_to_rgba(img, filename)
        vcode =  pp.cut_two_pics(new_rgba, filename)
        # import pdb
        # pdb.set_trace()
        # pp.remove_interferline(new_rgba)

        
        


