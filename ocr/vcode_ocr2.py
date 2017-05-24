#coding:utf-8
import os


def getverify():
    """
        @验证码识别命令 tesseract 图片名 生成文件名
        @ 图片名：默认为RandomNumber.gif 
        @生成文件名默认为result.txt
        @dos命令执行多条使用 &&连接
        @remove为防止验证码错误时，再次验证下载图片会因重名带来问题（测试中重名会自动覆盖）
    """
    dirpath = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(dirpath, 'new.png')
    cmd = "cd " + dirpath + " && tesseract new.png result"
    #print cmd
    os.system(cmd)
    resultpath = os.path.join(dirpath,"result.txt")
    with open(resultpath,"r") as f:
        verifyvalue = f.read()
    os.remove(image_path) 
    return verifyvalue

print getverify()