# __author__ = 'tonye0115'
# -*- coding: utf-8
from numpy import *
import matplotlib.pyplot as plt

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat

def gradAscent(dataMatIn, classLabels):
    """
    Logistic 回归梯度上升优化算法
    :param dataMatIn:
    :param classLabels:
    :return:
    """
    # 转化为NumPy矩阵的数据函数
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()
    maxCycles = 200  # 迭代次数
    m, n = shape(dataMatrix)  # 读取矩阵的长度
    alpha = 0.001  # 目标移动的步长
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (labelMat - h)
        weights += alpha * dataMatrix.transpose() * error
    return weights

def stocGradAscent0(dataMatrix, classLabels):
    m, n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i] * weights))
        error = classLabels[i] - h
        weights += alpha * error * dataMatrix[i]
    return weights

def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))

def plotBestFit(weights):
    dataMat, labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []

    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()





if __name__ == '__main__':
    dataArr, labelMat = loadDataSet()
    # weigits = gradAscent(dataArr, labelMat)
    weigits = stocGradAscent0(array(dataArr), labelMat)
    plotBestFit(weigits)