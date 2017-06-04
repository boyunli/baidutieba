# coding:utf-8

import os
import numpy as np
import struct
import PIL.Image
 
train_data_dir = os.path.join(os.path.dirname(__file__), "HWDB1.1trn_gnt_P1/")
test_data_dir = os.path.join(os.path.dirname(__file__), "HWDB1.1tst_gnt/")
data_dir = os.path.join(os.path.dirname(__file__), "data/")
TRAINDIR = os.path.join(data_dir, "train/")
TESTDIR = os.path.join(data_dir, "test/")
# 读取图像和对应的汉字
def read_from_gnt_dir(gnt_dir=train_data_dir):
    # import pdb
    # pdb.set_trace()
    
    def one_file(f):
        header_size = 10
        while True:
            header = np.fromfile(f, dtype='uint8', count=header_size)
            if not header.size: break
            sample_size = header[0] + (header[1]<<8) + (header[2]<<16) + (header[3]<<24)
            tagcode = header[5] + (header[4]<<8)
            width = header[6] + (header[7]<<8)
            height = header[8] + (header[9]<<8)
            if header_size + width*height != sample_size:
                break
            image = np.fromfile(f, dtype='uint8', count=width*height).reshape((height, width))
            yield image, tagcode

    for file_name in os.listdir(gnt_dir):
        if file_name.endswith('.gnt'):
            file_path = os.path.join(gnt_dir, file_name)
            with open(file_path, 'rb') as f:
                for image, tagcode in one_file(f):
                    yield image, tagcode
 
# 统计样本数
train_counter = 0
test_counter = 0
for image, tagcode in read_from_gnt_dir(gnt_dir=train_data_dir):
    tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312')
    # """
    # 提取点图像, 看看什么样
    if train_counter < 30000:
        im = PIL.Image.fromarray(image)
        im.convert('RGB').save(TRAINDIR + tagcode_unicode + str(train_counter) + '.png')
    # """
    train_counter += 1
for image, tagcode in read_from_gnt_dir(gnt_dir=test_data_dir):
    tagcode_unicode = struct.pack('>H', tagcode).decode('gb2312')
    if test_counter < 500:
        # import pdb
        # pdb.set_trace()
        im = PIL.Image.fromarray(image)
        im.convert('RGB').save(TESTDIR + tagcode_unicode + str(test_counter) + '.png')
    test_counter += 1

    
# 样本数
print(train_counter, test_counter)  # (448959, 223991)