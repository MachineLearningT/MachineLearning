# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-

from numpy import *

def loadDataSet():
    postingList = [
        ['my','my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 侮辱性词语 0 正常词语
    return postingList, classVec

def createVocabList(dataSet):
    """
    创建词汇表
    :param dataSet:
    :return:
    """
    vocabSet = set([])  # 创建不重复的空集合
    for doucument in dataSet:
        vocabSet = vocabSet | set(doucument)
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)  # 创建一个和词汇表等长的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def bagOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)  # 创建一个和词汇表等长的向量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    """
    朴素贝叶斯分类器训练函数
    :param trainMatrix: 文档矩阵
    :param trainCategory:
    :return:
    """
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    """
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    """
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]  # 侮辱性词语 矩阵+1
            p1Denom += sum(trainMatrix[i])  # 侮辱性类别总词数
        else:
            p0Num += trainMatrix[i]  # 正常词语 矩阵+1
            p0Denom += sum(trainMatrix[i])  # 正常词语总词数
    p0Vect = p0Num / p0Denom
    p1Vect = p1Num / p1Denom

    # 侮辱类概率
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    # return p0Vect, p1Vect, pAbusive
    return log(p0Vect), log(p1Vect), pAbusive

def classifyNB(newDoc, p0Vec, p1Vec, pAb):
   """
   朴素贝叶斯分类函数
   :param newDoc:
   :param p0Vec:
   :param p1Vec:
   :param pAb:
   :return:
   """
   p1 = sum(newDoc * p1Vec) + log(pAb)
   p0 = sum(newDoc * p0Vec) + log(1.0 - pAb)
   if p1 > p0:
       return 1
   else:
       return 0

def textParse(bigString):
    """
    接收一个大写字符串解析为字符串列表
    去掉少于两个字符的字符串
    将所有字符转为小写
    :param bigString:
    :return:
    """
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

if __name__ == '__main__':
    listOposts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOposts)
    trainMat = []
    bagTrainMat = []
    for postinDoc in listOposts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    for postinDoc in listOposts:
        bagTrainMat.append(bagOfWords2Vec(myVocabList, postinDoc))

    print trainMat
    print bagTrainMat

    p0Vect, p1Vect, pAbusive = trainNB0(trainMat, listClasses)
    print myVocabList
    print pAbusive
    print p0Vect
    print p1Vect

    testEntry = ['love', 'my', 'dalmation']
    newDoc = setOfWords2Vec(myVocabList, testEntry)
    print testEntry, 'classified as: ', classifyNB(newDoc, p0Vect, p1Vect, pAbusive)

    testEntry = ['stupid', 'garbage']
    newDoc = setOfWords2Vec(myVocabList, testEntry)
    print testEntry, 'classified as: ', classifyNB(newDoc, p0Vect, p1Vect, pAbusive)