# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-

from numpy import *

from knn import kNN

def classifyPerson():
    resultList = ['讨厌', '一般喜欢', '非常喜欢']
    ffMiles = float(raw_input("每年获得的飞行里程数："))
    percentTats = float(raw_input("玩视频游戏所耗时间百分比："))
    iceCream = float(raw_input("每周消费的冰激凌公升数："))

    datingDatamat, datingLabels = kNN.file2matrix('datingTestSet2.txt')  # 从文件中读取数据
    normMat, ranges, minValue = kNN.autoNorm(datingDatamat)  # 训练样本归一化特征值
    inArr = array([ffMiles, percentTats, iceCream])
    inArrAutoNorm = (inArr - minValue) / ranges   # 输入数据归一化特征值
    classifierResult = kNN.classify0(inArrAutoNorm, normMat, datingLabels, 3)
    print "喜欢程度:", resultList[classifierResult - 1]

if __name__ == '__main__':
    classifyPerson()