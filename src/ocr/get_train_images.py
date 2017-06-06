# coding:utf-8

import os
import sys
import logging
import logging.config

import cv2
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from spider.settings import LOGGING
from spider.settings import LOGGING
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('myocr')

BASEDIR = os.path.dirname(os.path.abspath(__file__))
VCODEDIR = os.path.join(BASEDIR, 'images/corr_vcode/')
TRAINDIR = os.path.join(BASEDIR, 'images/train/')

def CutImage(Bpp, filename):

    logger.debug('start cut {filename} to single vcode...'.format(filename=filename))
    shotname, extension = os.path.splitext(filename)

    img1 = np.zeros((72, 80))   #高/宽
    for i in range(0, 80):
        for j in range(0, 72):
            img1[j][i] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'1'+ extension, img1)

    img2 = np.zeros((72, 80))   #高/宽
    for i in range(80, 160):
        for j in range(0, 72):
            img2[j][i-80] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'2'+ extension, img2)

    img3 = np.zeros((72, 80))   #高/宽
    for i in range(160, 240):
        for j in range(0, 72):
            img3[j][i-160] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'3'+ extension, img3)

    img4 = np.zeros((72, 80))   #高/宽
    for i in range(0, 80):
        for j in range(72, 144):
            img4[j-72][i-0] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'4'+ extension, img4)

    img5 = np.zeros((72, 80))   #高/宽
    for i in range(80, 160):
        for j in range(72, 144):
            img5[j-72][i-80] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'5'+ extension, img5)

    img6 = np.zeros((72, 80))   #高/宽
    for i in range(160, 240):
        for j in range(72, 144):
            img6[j-72][i-160] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'6'+ extension, img6)

    img7 = np.zeros((72, 80))   #高/宽
    for i in range(0, 80):
        for j in range(144, 216):
            img7[j-144][i-0] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'7'+ extension, img7)

    img8 = np.zeros((72, 80))   #高/宽
    for i in range(80, 160):
        for j in range(144, 216):
            img8[j-144][i-80] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'8'+ extension, img8)

    img9 = np.zeros((72, 80))   #高/宽
    for i in range(160, 240):
        for j in range(144, 216):
            img9[j-144][i-160] = Bpp[j][i]
    cv2.imwrite(TRAINDIR+shotname+'9'+ extension, img9)

    logger.debug('has cuted {filename} to single vcode...'.format(filename=filename))
    return 
    
    
if __name__ == '__main__':
    vcodes = os.listdir(VCODEDIR)
    for filename in vcodes:
        file_path = os.path.join(VCODEDIR, filename)
        Img = cv2.imread(file_path, 0)
        cut_images = CutImage(Img, filename)
