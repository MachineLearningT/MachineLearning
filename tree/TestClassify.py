# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-

from tree import trees
from tree import treePlotter
from numpy import *

def getDecisionList(myTree):
    """
    获取所有决策节点
    """
    decisionList = []
    firstStr = myTree.keys()[0]
    decisionList.append(firstStr)
    secondDict = myTree[firstStr]

    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':#test to see if the nodes are dictonaires, if not they are leaf nodes
            decisionList.extend(getDecisionList(secondDict[key]))
    return decisionList

def queryResult(myTree, vLabels, queryDict):
    # 取出按树结构排列的属性名称
    decisionList = getDecisionList(myTree)
    # 取出按树结构排列的属性值
    queryList = []
    for i in decisionList:
        queryList.append(queryDict[i])
    return trees.classify(myTree, decisionList, queryList)


if __name__ == '__main__':
    """
    测试决策树的分类函数
    """
    dataSet, labels = trees.createDataSet()
    vLabel = labels[:]
    print 'vLabels:', vLabel
    myTree = trees.createTree(dataSet, labels)
    queryDict = {'flippers': 1, 'no surfacing': 0}
    print ' query result: %s ' % queryResult(myTree, vLabel, queryDict)