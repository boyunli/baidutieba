# -*- coding: utf_8 -*-
from PIL import Image
import cv2

def InterferLine(Bpp):
        
        for i in range(0, 41):
            for j in range(0,Bpp.shape[0]):    #Bpp.shape=(320L, 240L) 高、宽
                Bpp[j][i]=255                  #白色
        for i in range(161,Bpp.shape[1]):
            for j in range(0,Bpp.shape[0]):
                Bpp[j][i]=255        
        m=1
        n=1
        import pdb
        pdb.set_trace()
        for i in range(41,161):
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
        cv2.imwrite('2.jpg',Bpp)
        return Bpp

if __name__ == '__main__':
    filename = '1.jpg'
    Img = cv2.imread(filename)
    InterferLine(Img)