# __author__ = 'tonye0115'
# -*- coding: utf-8 -*-
from numpy import *

def loadDateSet(fileName):
    '''
    从文本文件中构建矩阵
    :param fileName:
    :return:
    '''
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return mat(dataMat)

def disEclud(vecA, vecB):
    '''
    计算两个向量的距离
    :param vecA:
    :param vecB:
    :return:
    '''
    return sqrt(sum(power(vecA-vecB, 2)))

def randCent(dataSet, k):
    '''
    构建簇质心
    :param dataSet:
    :param k:k个随机质心集合
    :return:
    '''
    n = shape(dataSet)[1]  # shape获取矩阵的行列属性
    centroids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataMat[:, j])
        rangeJ = float(max(dataMat[:, j]) - minJ)
        radm = random.rand(k, 1) # 产生k个0到1之间的随机数
        centroids[:, j] = minJ + rangeJ * radm
    return centroids

def kMeans(dataSet, k, distMeas=disEclud, createCent=randCent):
    '''
    k-均值聚类算法
    :param dataSet:
    :param k:
    :param distMeas:
    :param createCent:
    :return:
    '''
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m , 2)))
    centroids = createCent(dataSet, k)
    print centroids
    clusterChanged = True

    while clusterChanged:
        clusterChanged = False

        # 分别标记每个点最近的质心
        for i in range(m):
            minDist = inf   # 正无穷大
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:  # while循环两遍，第二遍做校验
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2  # ** 表示乘方
        #print clusterAssment

        # 循环质心，更新质心位置
        for cent in range(k):
            # 取出按质心分类的点
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)  # 按列放心计算平均值
    return centroids, clusterAssment


def biKmeans(dataSet, k, distMeas=disEclud):
    '''
    二分k-均值聚类算法
    :param dataSet:
    :param k:
    :param distMeas:
    :return:
    '''
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))

    #创建初始簇
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]
    for j in range(m):
        clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            # 尝试划分每一簇
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0], :]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
            print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
            if(sseSplit + sseNotSplit) < lowestSSE:  # 如果划分的SSE值最小， 则本次划分被保存
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        # 更新簇的分配结果
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit

        print 'the bestCentToSplit is: ', bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClustAss)

        centList[bestCentToSplit] = bestNewCents[0, :]
        centList.append(bestNewCents[1, :])

        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss

        print centList


if __name__ == '__main__':
   dataMat = loadDateSet('testSet2.txt')
   '''
   print dataMat

   print min(dataMat[:, 0])
   print max(dataMat[:, 0])
   print min(dataMat[:, 1])
   print max(dataMat[:, 1])
   '''
   #print randCent(dataMat, 2)


   #print disEclud(dataMat[0], dataMat[1])

   #print kMeans(dataMat, 4)

   biKmeans(dataMat, 3)