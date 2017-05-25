#coding:utf-8
import os
import cv2
import time
import random

import numpy as np
# from matplotlib import pyplot as plt
from PIL import Image,ImageEnhance,ImageFilter


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
        cv2.imwrite('test/1.png',Bpp[1])
        return Bpp[1]

    def InterferLine(self,Bpp,filename):
       
        for i in range(0,76):
            for j in range(0,Bpp.shape[0]):    #Bpp.shape=(320L, 240L) 高、宽
                Bpp[j][i]=255                  #白色
        for i in range(161,Bpp.shape[1]):
            for j in range(0,Bpp.shape[0]):
                Bpp[j][i]=255        
        m=1
        n=1
        import pdb
        pdb.set_trace()
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
        cv2.imwrite('test/2.png',Bpp)
        return Bpp

    def CutImage(self,Bpp,filename):
        outpath = 'test/'
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
    PP=PreProcess()
    filename = 'vcode_8.png'
    Img = cv2.imread(filename)
    GrayImage=PP.ConvertToGray(Img,filename)
    Bpp=PP.ConvertTo1Bpp(GrayImage,filename)
    Bpp_new=PP.InterferLine(Bpp,filename)
    b=PP.CutImage(Bpp_new,filename)