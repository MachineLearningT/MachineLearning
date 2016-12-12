# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-
from math import log
import operator

def calcShannonEnt(dataSet):
    """
    计算给定数据集的香农熵
    :param dataSet:按特征划分的数据集
    :return: 信息熵
    """
    numEntries = len(dataSet)
    lablesCounts = {}
    # 为所有可能的分类创建数据字典
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in lablesCounts.keys():
            lablesCounts[currentLabel] = 0
        lablesCounts[currentLabel] += 1

    # 计算所有类别所有可能只包含的信息期望值
    shannonEnt = 0.0
    for key in lablesCounts:
        prob = float(lablesCounts[key]) / numEntries  # 选择该分类的概率
        shannonEnt -= prob * log(prob, 2)  # 以2为底求对数
    return shannonEnt

def splitDateSet(dataSet, axis, value):
    """
    按照给定特征划分数据集
    :param dataSet:待划分的数据集
    :param axis:划分数据集的特征
    :param value:需要返回的特征的值
    :return:特征数据集
    """
    retDataSet = []  #创建新的数据集对象
    for featVec in dataSet:
        if featVec[axis] == value:
            # 抽取除指定特征外的其他集合数据，重新组成一个新的数据集
            reduceFeatVec = featVec[:axis]
            reduceFeatVecAfter = featVec[axis+1:]
            reduceFeatVec.extend(reduceFeatVecAfter)
            retDataSet.append(reduceFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    """
    选择最好的数据集划分方式
    :param dateSet:按照给定特征划分数据集
    :return:
    """
    numFeatures = len(dataSet[0]) - 1  # 当前数据集包含的特征属性个数
    baseEntropy = calcShannonEnt(dataSet)  # 计算整个数据集的原始香农熵 (最初的无序度量值)

    # 最好的信息增益  (原始香农熵大于新香农熵，差值越大(信息增益)越好)
    # 原始香农熵值高，因为混合的数据多导致的
    bestInfoGain = 0.0
    bestFeature = -1

    for i in range(numFeatures):
        # 使用列推导模式创建列表
        # 将数据集中所有第i个特征值或者可能从在的值写入的这个新的list中
        featList = [example[i] for example in dataSet]
        #创建唯一的分类标签列表
        uniqueVals = set(featList)  # 创建set集合 (无序不重复集合)

        #计算每种划分方式的信息熵
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDateSet(dataSet, i, value)
            # 计算数据集的新熵
            # 对唯一特征值得到的熵求和
            # 此处乘以百分比，再累加，是针对原始香农熵来说的
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        #计算出最好的信息增益(比较出最小的香农熵)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    """
    遍历完所有类标签返回出现次数最多的分类名称
    例如：使用完所有的标签，任然不能划分唯一类型的分组 --￥ [['yes'], ['yes'], ['no']]
    :param classList:
    :return:
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    print "--￥ %s" % dataSet
    """
    创建数的函数代码
    :param dataSet:
    :param labels:
    :return:
    """
    classList = [example[-1] for example in dataSet]
    # 递归函数的停止条件1 判断类别完全相同则停止划分
    if classList.count(classList[0]) == len(classList):
        print "####^ %s" % classList[0]
        return classList[0]

    # 递归函数的停止条件2 使用完所有特征，任然不能将数据集划分成仅包含唯一类别的分组
    if len(dataSet[0]) == 1:
        print "**** %s" % dataSet[0]
        return majorityCnt(classList)  # 挑选出现次数最多的类别做为返回值

    bestFeat = chooseBestFeatureToSplit(dataSet)  # 选择最好的划分方式
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])  # 删除标签集合 最好的特征属性
    featValues = [example[bestFeat] for example in dataSet]  # 获取最好的特征属性下 所有特征值
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDateSet(dataSet, bestFeat, value), subLabels)
    return myTree


def classify(inputTree, featLabels, inputVec):
    """
    使用决策树的分类函数
    :param inputTree:
    :param featLabels: 原始分类
    :param inputVec: 查询的属性（按照tree排列）
    :return:
    """
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if inputVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, inputVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]

    labels = ['no surfacing', 'flippers']
    return dataSet, labels

if __name__ == '__main__':
    dataSet, labels = createDataSet()
    print labels
    # dataSet[0][-1] = 'maybe'
    print chooseBestFeatureToSplit(dataSet)
    print createTree(dataSet, labels)
