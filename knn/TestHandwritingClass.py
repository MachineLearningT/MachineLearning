# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-
from os import listdir
from numpy import *
from knn import kNN

def handwritingClass():
    """
    手写数字识别系统
    k-近邻算法缺点：
    1.算法的执行效率不高
    2.需要为训练数据集准备很大的存储空间
    3.可以完成很多分类任务，无法给出任何数据的基础结构信息，
    无法知晓平均实例样本和典型实例样本具体有什么特征
    :return:
    """
    trainingFileList = listdir('trainingDigits')  # 获取目录内容 (样本数据)
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))  # 创建一个m行1024列的训练矩阵，每行存储一个图像

    hwLabels = []  # 分类数字集合

    # 从文件名解析分类数字
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]  # 获取文件名
        classNumStr = int(fileStr.split('_')[0])  # 从文件名解析分类数字
        hwLabels.append(classNumStr)
        trainingMat[i, :] = kNN.img2vector('trainingDigits/%s' % fileNameStr)  # 每行存储一个图像

    # 测试数据目录
    testFileList = listdir('testDigits')
    mTest = len(testFileList)

    errorCount = 0.0

    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = kNN.img2vector('testDigits/%s' % fileNameStr)
        classifierResult = kNN.classify0(vectorUnderTest, trainingMat, hwLabels, 3)

        print 'the classifier came back with: %d, the real answer is: %d' % (classifierResult, classNumStr)
        if classifierResult != classNumStr:
            errorCount += 1.0
    print "the total number of errors is: %d" % errorCount
    print "the total error rate is : %.2f%%" % float(errorCount / mTest) * 100



if __name__ == '__main__':
    handwritingClass()