# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-

from baye import bayes
from numpy import *

def spamTest():
    #导入并解析文本文件
    docList = []; classList = []; fullTest = []
    for i in range(1, 26):
        wordList = bayes.textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullTest.extend(wordList)
        classList.append(1)
        wordList = bayes.textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullTest.extend(wordList)
        classList.append(0)
    print docList
    print fullTest
    print "classList %s" % classList

    # 创建词不重复列表
    vocabList = bayes.createVocabList(docList)
    print vocabList

    # 随机构建训练集
    trainingSet = range(50); testSet = []
    for i in range(10):
        randomIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randomIndex])
        del(trainingSet[randomIndex])
    print "testSet %s" % testSet

    # 构建测试集
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bayes.setOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = bayes.trainNB0(array(trainMat), array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = bayes.setOfWords2Vec(vocabList, docList[docIndex])
        if bayes.classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is : ', float(errorCount)/len(testSet)

if __name__ == '__main__':
    spamTest()