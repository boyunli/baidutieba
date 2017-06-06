#coding:utf-8
import os
import sys
import time
import random
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
VCODEDIR = os.path.join(BASEDIR, 'images/vcode/')
BPPDIR = os.path.join(BASEDIR, 'images/bpp/')
MOVE_TNTERFER = os.path.join(BASEDIR, 'images/move_interfer/')
CUTED_SINGLEDIR = os.path.join(BASEDIR, 'images/cuted_single/')
CUTED_HALFDIR = os.path.join(BASEDIR, 'images/cuted_half/')
TRAINDIR = os.path.join(BASEDIR, 'train/')
if not os.path.exists(CUTED_SINGLEDIR):
    os.makedirs(CUTED_SINGLEDIR)

class PreProcess(object):
    """description of class"""

    def ConvertToGray(self,Image,filename):
        '''
        灰度化
        '''
        logger.debug('start convert {} to gray...'.format(filename))
        GrayImage=cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY)
        logger.debug('has converted {} to gray...'.format(filename))
        return GrayImage
       
    def ConvertTo1Bpp(self,GrayImage,filename):
        '''
        二值化
        '''
        logger.debug('start convert {gray} to 1bpp...'.format(gray=filename))
        Bpp=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
        file_path = os.path.join(BPPDIR, filename)
        cv2.imwrite(file_path, Bpp[1])
        # cv2.imwrite('test/bpp.png', Bpp[1])
        logger.debug('has converted {gray} to 1bpp...'.format(gray=filename))
        return Bpp[1]

    def RemoveInterferLine(self,Bpp,filename):
        '''
        去干扰线
        '''
        logger.debug('start remove {filename} interferline...'.format(filename=filename))
        for i in range(0, 52):
            for j in range(0,Bpp.shape[0]):    #Bpp.shape=(320L, 240L) 高、宽
                Bpp[j][i]=255                  #白色
        for i in range(200,Bpp.shape[1]):
            for j in range(0,Bpp.shape[0]):
                Bpp[j][i]=255        
        m=1
        n=1
      
        for i in range(52, 240):
            while(m<Bpp.shape[0]-1):
                if Bpp[m][i]==0:
                    if Bpp[m+1][i]==0:
                        n=m+1
                    elif m>0 and Bpp[m-1][i]==0:
                        n=m
                        m=n-1
                    else:
                        n=m+1
                    break
                elif m!=Bpp.shape[0]:
                    l=0
                    k=0
                    ll=m
                    kk=m
                    while(ll>0):
                        if Bpp[ll][i]==0:
                            ll=11-1
                            l=l+1
                        else:
                            break
                    while(kk>0):
                        if Bpp[kk][i]==0:
                            kk=kk-1
                            k=k+1
                        else:
                            break
                    if (l<=k and l!=0) or (k==0 and l!=0):
                        m=m-1
                    else:
                        m=m+1
                else:
                    break
                #endif
            #endwhile
            if m>0 and Bpp[m-1][i]==0 and Bpp[n-1][i]==0:
                continue
            else:
                Bpp[m][i]=255
                Bpp[n][i]=255
            #endif
        #endfor
        file_path = os.path.join(MOVE_TNTERFER, filename)
        cv2.imwrite(file_path, Bpp)
        # cv2.imwrite('test/inter.png', Bpp)
        logger.debug('has removed {filename} interferline...'.format(filename=filename))
        return Bpp

    def CutImage(self, Bpp, filename):
        '''
        切图并标准化：采用二分法
        '''
        logger.debug('start cut {filename} to single vcode...'.format(filename=filename))
        # CUTED_SINGLEDIR = CUTED_HALFDIR = 'test/'
        # 先一分为二：每部分两个字
        shotname, extension = os.path.splitext(filename)
        import pdb
        pdb.set_trace()
        left = np.zeros((Bpp.shape[0], 82))
        for i in range(42,124):
            for j in range(0,Bpp.shape[0]):
                left[j][i-43] = Bpp[j][i]
        cv2.imwrite(CUTED_HALFDIR+shotname+'1'+ extension, left)
        left_32 = cv2.resize(left,(32,32), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(TRAINDIR+shotname+'1'+ extension, left_32)

        right = np.zeros((Bpp.shape[0],92))
        for i in range(122,214):
            for j in range(0,Bpp.shape[0]):
                right[j][i-122] = Bpp[j][i]
        cv2.imwrite(CUTED_HALFDIR+shotname+'2'+ extension, right)
        # 再二分为四， 每部分一个字
        left_1 = np.zeros((left.shape[0],40))
        for i in range(0, 40):
            for j in range(0,left.shape[0]):
                left_1[j][i-0] = left[j][i]
        cv2.imwrite(CUTED_SINGLEDIR+shotname+ '11'+extension, left_1)

        left_2=np.zeros((left.shape[0],40))
        for i in range(41, 81):
            for j in range(0,left.shape[0]):
                left_2[j][i-41]=left[j][i]
        cv2.imwrite(CUTED_SINGLEDIR+shotname+ '12'+extension, left_2)

        right_1=np.zeros((right.shape[0],40))
        for i in range(0, 40):
            for j in range(0,right.shape[0]):
                right_1[j][i-0]=right[j][i]
        cv2.imwrite(CUTED_SINGLEDIR+shotname+ '21'+extension, right_1)

        right_2=np.zeros((right.shape[0],40))
        for i in range(38, 78):
            for j in range(0,right.shape[0]):
                right_2[j][i-38]=right[j][i]
        cv2.imwrite(CUTED_SINGLEDIR+shotname+ '22'+extension, right_2)

        cuted_images = [left, right, left_1, left_2, right_1, right_2]
        logger.debug('has cuted {filename} to single vcode...'.format(filename=filename))
        return cuted_images
    
    def RotateImage(self, cuted_image, filename):
        '''
        扭转字体
        '''
        pass
    
    
if __name__ == '__main__':
    vcodes = os.listdir(VCODEDIR)
    PP = PreProcess()
    for filename in vcodes:
        file_path = os.path.join(VCODEDIR, filename)
        Img = cv2.imread(file_path)
        GrayImage = PP.ConvertToGray(Img,filename)
        Bpp = PP.ConvertTo1Bpp(GrayImage,filename)
        remove_interferline = PP.RemoveInterferLine(Bpp,filename)
        cut_images = PP.CutImage(remove_interferline,filename)

    # filename = 'vcode_1622.png'
    # Img = cv2.imread(filename)
    # GrayImage=PP.ConvertToGray(Img,filename)
    # Bpp=PP.ConvertTo1Bpp(GrayImage,filename)
    # bpp_new=PP.RemoveInterferLine(Bpp,filename)
    # cuted_image = PP.CutImage(bpp_new,filename)
    # rotate_image = PP.RotateImage(cuted_image, filename)
