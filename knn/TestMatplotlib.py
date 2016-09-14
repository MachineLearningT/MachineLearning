# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from numpy import *

from knn import kNN

if __name__ == '__main__':
    # 使用Matplotlib创建散列图
    print("aaa")
    datingDataMat, datingLabels = kNN.file2matrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)    #将画布分为1行1列，从到右从上到下显示第1块
    # 绘制散列点
    # 绘制尺寸大小相同，色彩相同的散列点
    #ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2])
    # 绘制尺寸大小不同、色彩相同的散列点
    #ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2], 15.0 * array(datingLabels))
    # 绘制尺寸大小不同、色彩不同的散列点
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()



