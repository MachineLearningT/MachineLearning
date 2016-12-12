# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-

from numpy import *
from tree import trees
from tree import treePlotter
from tree import TestClassify


def classifyPerson():
    fr = open('lenses.txt')
    lensesMat = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    print lensesMat, lensesLabels
    myTree = trees.createTree(lensesMat, lensesLabels)
    print myTree
    queryDict = {'age': 'young', 'prescript': 'myope', 'astigmatic': 'no', 'tearRate': 'reduced'}
    print ' query result: %s ' % TestClassify.queryResult(myTree, ['age', 'prescript', 'astigmatic', 'tearRate'], queryDict)
    treePlotter.createPlot(myTree)


if __name__ == '__main__':
    classifyPerson()