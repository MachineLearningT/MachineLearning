# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-
"""
使用贝朴素叶斯分类器从个人广告中获取区域倾向
"""
from baye import bayes
import feedparser
from numpy import *

def localWords(feed1, feed0):
    import feedparser
    docList = []; classList = []; fullText = []
    minLen = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLen):
        wordList = bayes.textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = bayes.textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = bayes.createVocabList(docList)
    top30Words = calcMostFreq(vocabList, fullText)

    # 去掉出现次数最多的那些词
    for pairW in top30Words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])

    # 随机构建训练集和测试集
    trainingSet = range(2 * minLen)
    testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    # 训练分类器，计算概率
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bayes.bagOfWords2Vec(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V, p1V, pSpam = bayes.trainNB0(array(trainMat), array(trainClasses))


    # 测试分类数据 错误率
    errorCount = 0
    for docIndex in testSet:
        wordVector = bayes.bagOfWords2Vec(vocabList, docList[docIndex])
        if bayes.classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
             errorCount += 1
    print 'the error rate is: ', float(errorCount) / len(testSet)
    return vocabList, p0V, p1V




def calcMostFreq(vocabList, fullText):
    """
    遍历词汇表的每个单词，统计它在文本中出现的次数，
    然后根据出现的次数从高低对词典进行排序
    最后返回排序最高的30个单词
    :param vocabList:词汇表
    :param fullText:
    :return:
    """
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedFreq[:30]

def getTopWords(ny, sf):
    """
    最具表征性的词汇显示函数
    :param ny:
    :param sf:
    :return:
    """
    vocabList, p0V, p1V = localWords(ny, sf)
    topNY = []; topSF = []
    for i in range(len(p0V)):
        if p0V[i] > -6.0:
            topSF.append((vocabList[i], p0V[i]))
        if p1V[i] > -6.0:
            topNY.append((vocabList[i], p1V[i]))
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
    print "SF**********************"
    for item in sortedSF:
        print item[0]

    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    print "NF**********************"
    for item in sortedNY:
        print item[0]



if __name__ == '__main__':
    ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
    sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
    getTopWords(ny, sf)