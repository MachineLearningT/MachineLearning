# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-

from numpy import *
from tree import trees
from tree import treePlotter

def classifyPerson():
    fr = open('lenses.txt')
    lensesMat = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    print lensesMat, lensesLabels
    myTree = trees.createTree(lensesMat, lensesLabels)
    print myTree
    treePlotter.createPlot(myTree)

if __name__ == '__main__':
    classifyPerson()