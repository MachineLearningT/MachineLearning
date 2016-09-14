# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-
from numpy import *
import operator
from os import listdir

def __init__(self):
    pass

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'B', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    """
    k-近邻算法

    :param inX:输入向量
    :param dataSet:输入的训练样本集
    :param labels:标签向量
    :param k:确定前k个点所在类别的出现频率
    :return:返回前k个点出现频率最好的类别作为当前的预测分类
    """
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines, 3))         #创建0矩阵
    classLabelVector = []                       #prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]  #对矩阵赋值
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def autoNorm(dataSet):
    """
    归一化特征
    newValue = (oldValue - min)/(max - min)
    """
    minVals = dataSet.min(0)    # 每一列的最小是
    maxVals = dataSet.max(0)    # 每一列的最大值
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))  # 创建0矩阵  (shape函数 读取矩阵的长度)
    m = dataSet.shape[0]  # 获取矩阵长度的第一个参数 (行数)
    normDataSet = dataSet - tile(minVals, (m, 1))   # tile函数 重复某个数组 (m,1) - m在行的数据上重复，1在列的数据上不重复
    normDataSet = normDataSet/tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def datingClassTest():
    """
    使用错误率测试分类器
    :return:
    """
    hoRatio = 0.10  # 10%的是测试数据，用于测试分类器
    datingDatamat, datingLabels = file2matrix('datingTestSet2.txt')  # 从文件中读取数据

    normMat, ranges, minValue = autoNorm(datingDatamat)  # 归一化特征值

    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)  # 参与测试数据个数 10% 100个

    errorCount = 0.0

    for i in range(numTestVecs):
        inX = normMat[i, :]  # 随机测试数据
        dataSet = normMat[numTestVecs:m, :]  # 分类器的训练样本 90%  900个 从numTestVecs到m
        labels = datingLabels[numTestVecs:m]  # 训练样本的标签向量
        # 调用k近邻算法的原始分类器
        classifierResult = classify0(inX, dataSet, labels, 3)
        print "the classifiter came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print "the total error rate is: %.2f %%" % (errorCount / float(numTestVecs) * 100)


def img2vector(filename):
    """
     将一个32x32的二进制图像矩阵转换为1x1024的向量
    :param filename: 输入文件名称
    :return: 返回 1x1024 向量
    """
    retrunVect = zeros((1, 1024))  # 创建1x1024 0矩阵
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            retrunVect[0, 32 * i + j] = int(lineStr[j])
    return retrunVect


if __name__ == '__main__':
    datingClassTest()
    testVector = img2vector('testDigits/0_13.txt')
    print testVector[0, 0:32]
    print testVector[0, 32:63]
