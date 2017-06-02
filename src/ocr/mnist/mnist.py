# coding:utf-8

import pylab
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential   #神经网络层的线性栈
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D   # 卷积层,帮助训练图片数据
from keras.utils import np_utils   # 数据转换工具
from keras.datasets import mnist


np.random.seed(123)
(X_train, y_train), (X_test, y_test) = mnist.load_data()
# print X_train.shape  #(60000L, 28L, 28L)   训练集中有 60000 个样本, 每张图片都是 28*28 像素大小
# print X_test.shape   #(10000L, 28L, 28L)   测试集中有 10000 个样本
import pdb
pdb.set_trace()
print X_train[0]
plt.imshow(X_train[0])
pylab.show()   

#将数据集从 (n, width, height) 转换成 (n, depth, width, height)
X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)
print X_train.shape  # (60000L, 1L, 28L, 28L)


X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255

print y_train[:10]

Y_train = np_utils.to_categorical(y_train, 10)
Y_test = np_utils.to_categorical(y_test, 10)

print Y_train.shape
print Y_train[:10]

#定义模型架构
model = Sequential()
#layer1-conv1 
model.add(Convolution2D(32, 3, 3, activation='relu', input_shape=(1, 28, 28)))
print model.output_shape #  (None, -1, 26, 32)
# layer2-conv2  
model.add(Convolution2D(32, 3, 3, activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# layer43 
model.add(Flatten())
model.add(Dense(128, activation='relu'))
# layer4-fully connect
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', 
              metrics=['accuracy'])

# model.fit(X_train, Y_train,
#           batch_size=32, nb_epoch=10, verbose=1)

# score = model.evaluate(X_test, Y_test, verbose=0)

