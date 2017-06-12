#coding:utf-8
import os
import logging.config

from PIL import Image
from svmutil import *
from svm import *

BASEDIR = os.path.dirname(os.path.abspath(__file__))
TRAINDIR = os.path.join(BASEDIR, 'images/train/')
TESTDIR = os.path.join(BASEDIR, 'images/test/')

def get_feature(imgname, img1):
    '''
    获取指定图片的特征值，
    按照每排的像素点，高度为72,则有72个维度，
    宽度为80,则有80列， 总共152个维度
    '''

    width, height = img1.size
    pixel_cnt_list = []
    
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img1.getpixel((x, y)) == 0: #黑色
                pix_cnt_x += 1
        pixel_cnt_list.append(pix_cnt_x)
    
    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img1.getpixel((x, y)) == 0: #黑色
                pix_cnt_y += 1
        pixel_cnt_list.append(pix_cnt_y)

    # 生成LibSVM格式的训练数据
    #with open('train_pix_feature_xy.txt', 'a') as f:
    with open('last_test_pix_xy_new.txt', 'a') as f:
        label = imgname.split('_')[0]
        f.write(label)
        for i, v in enumerate(pixel_cnt_list):
            f.write(' {}:{}'.format(i+1, v))
        f.write('\n')

    #print pixel_cnt_list
    #print len(pixel_cnt_list)
    return pixel_cnt_list


def train_svm_model():
    '''
    模型训练
    训练并生成model文件
    '''
    y, x = svm_read_problem(os.path.join(BASEDIR, 'train_pix_feature_xy.txt'))
    model = svm_train(y, x)
    svm_save_model('model_file', model)

def svm_model_test():
    '''
    使用测试集测试模型
    '''
    yt, xt = svm_read_problem(os.path.join(BASEDIR, 'last_test_pix_xy_new.txt'))
    model = svm_load_model('model_file')
    p_label, p_acc, p_val = svm_predict(yt, xt, model)#p_label即为识别的结果

    print p_label

if __name__ == '__main__':
    #imgs= os.listdir(TRAINDIR)
    #imgs= os.listdir(TESTDIR)
    #for imgname in imgs:
    #    img_path = os.path.join(TRAINDIR, imgname)
    #    image = Image.open(img_path)
    #    #import pdb
    #    #pdb.set_trace()
    #    img1 = image.convert('1')  # 图片二值化
    #    img1.save(img_path)
    #    get_feature(imgname, img1)
    train_svm_model()



