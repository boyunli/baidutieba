# coding:utf-8

import numpy as np

class Network(object):

    def __init__(self, sizes):
        # sizes：每层神经元的个数, 比如：[2,3,1]
        self.num_layers = len(sizes)  # 神经网络的层数
        self.sizes = sizes
        # 在神经元和下一个神经元之间的那条线，都在进行着权重weight和偏向bias的更新，以生成下一个神经元的值
        # 随机生成权重和偏向的初始值，介于0-1
        # np.random.randn(y,1): 随机从正态分布（均值0,方差1）中生成
        # weights[0] 指的是连接第一层和第二层的权重
        self.biases = [np.random.randn(y,1) for y in sizes[1:]]
        self.weights = [np.random.randn(y,x)
                        for x,y in zip(sizes[:-1], sizes[1:])]


    def feedforward(self, a):
        '''
        向前传递
        return the output of the network if 'a' is input.
        '''
        for b,w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w,a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        '''
        随机梯度下降算法
        mini_batch_size: 将训练实例分成不同batch进行训练，避免训练集数量过大
        '''
        if test_data: n_test = len(test_data)
        n = len(traning_data)
        for j in xrange(epochs):
            # random.shuffle :洗牌, 打乱训练集里的数据, 达到从训练集中随机提取数据
            random.shuffle(traning_data)
            mini_batches = [
                    training_data[k:k+mini_batch_size]
                    for k in xrange(0, n, mini_batch_size)]
            for mini_batch in mini_batch_sizes:
                self.update_mini_batch(mini_batch, eta)  #更新权重和偏向 
            if test_data:
                print "Epoch {0}:{1} / {2}".format(
                        j, self.evaluate(test_data), n_test)
            else:
                print "Epoch {0} complete".format(j)
    
    def update_mini_batch(self, mini_batch, eta):
        '''
        update the network's weights and biases by applying gradient
        descent using backpropagation to a single mini batch.
        The 'mini_batch' is a list of typle '(x,y)', and 'eta' is the
        learning rate.
        '''
        nabla_b = [np.zeros(b,shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # x是 28*28 的像素点， y是0-9中的某个分类
        for x, y in mini_batch:
            # delta_nabla_b, delta_nabla_w 分别是bias和weight的偏导数
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [ w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [ b-(eta/len(mini_batch))*nb
                        for b, nb in zip(self.biases, nabla_b)]








































