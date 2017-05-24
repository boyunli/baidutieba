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
import logging
import logging.config

from PIL import Image
import cv2
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from spider.settings import LOGGING
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('myocr')

#因获取的验证码全部为灰度图，且基本没有噪点，所以无需二值化和去噪， 直接进行去干扰线

class PreProcess(object):
    """description of class"""

    def ConvertToGray(self,Image,filename):
        '''
        灰度化
        '''
        GrayImage=cv2.cvtColor(Image,cv2.COLOR_BGR2GRAY)
        return GrayImage
       
    def ConvertTo1Bpp(self,GrayImage,filename):
        '''
        二值化
        '''
        Bpp=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)
        cv2.imwrite('D://'+'1.jpg',Bpp[1])
        return Bpp
    
    def covert_to_opacity(self, image):
        width, height, z =  img.shape  #高、宽、通道3
            # threshold = 100
        for i in xrange(width):
            for j in xrange(height):
                pass

    def InterferLine(self,Bpp,filename):
        '''
        去干扰线
        '''
        for i in range(0,76):
            for j in range(0,Bpp.shape[0]):
                Bpp[j][i]=255
        for i in range(161,Bpp.shape[1]):
            for j in range(0,Bpp.shape[0]):
                Bpp[j][i]=255        
        m=1
        n=1
        for i in range(76,161):
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
        return Bpp

    def CutImage(self,Bpp,filename):
        b1=np.zeros((Bpp.shape[0],20))
        for i in range(78,98):
            for j in range(0,Bpp.shape[0]):
                b1[j][i-78]=Bpp[j][i]
        cv2.imwrite(outpath+filename.decode('gbk')[0].encode('gbk')+'_'+'%d' %(time.time()*1000)+str(random.randint(1000,9999))+'.png',b1)

        b2=np.zeros((Bpp.shape[0],19))
        for i in range(99,118):
            for j in range(0,Bpp.shape[0]):
                b2[j][i-99]=Bpp[j][i]
        cv2.imwrite(outpath+filename.decode('gbk')[1].encode('gbk')+'_'+'%d' %(time.time()*1000)+str(random.randint(1000,9999))+'.png',b2)

        b3=np.zeros((Bpp.shape[0],19))
        for i in range(119,138):
            for j in range(0,Bpp.shape[0]):
                b3[j][i-119]=Bpp[j][i]
        cv2.imwrite(outpath+filename.decode('gbk')[2].encode('gbk')+'_'+'%d' %(time.time()*1000)+str(random.randint(1000,9999))+'.png',b3)

        b4=np.zeros((Bpp.shape[0],19))
        for i in range(139,158):
            for j in range(0,Bpp.shape[0]):
                b4[j][i-139]=Bpp[j][i]
        cv2.imwrite(outpath+filename.decode('gbk')[3].encode('gbk')+'_'+'%d' %(time.time()*1000)+str(random.randint(1000,9999))+'.png',b4)
        #return (b1,b2,b3,b4)



if __name__ == '__main__':
    PP = PreProcess()
    import pdb
    pdb.set_trace()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pic_dir = os.path.join(base_dir, 'test/')
    vcode_pics = os.listdir(pic_dir)
    for filename in vcode_pics:
        img = cv2.imread(pic_dir+filename)  #太坑，此处inpath不能包含中文路径
        # GrayImage = PP.ConvertToGray(img, filename)
        Bpp = PP.ConvertTo1Bpp(img, filename)
        Bpp_new = PP.InterferLine(Bpp, filename)
        b = PP.CutImage(Bpp_new, filename)

