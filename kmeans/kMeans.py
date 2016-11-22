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
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        radm = random.rand(k, 1)  # 产生k个0到1之间的随机数
        centroids[:, j] = minJ + rangeJ * radm
    return centroids

#2维数据聚类效果显示
def datashow(dataSet,k,centroids,clusterAssment):  #二维空间显示聚类结果
    from matplotlib import pyplot as plt
    num,dim=shape(dataSet)  #样本数num ,维数dim

    if dim!=2:
        print 'sorry,the dimension of your dataset is not 2!'
        return 1

    marksamples=['or','ob','og','ok','^r','sb','<g'] #样本图形标记
    if k>len(marksamples):
        print 'sorry,your k is too large,please add length of the marksample!'
        return 1

    #绘所有样本
    for i in range(num):
        markindex=int(clusterAssment[i,0])#矩阵形式转为int值, 簇序号
        #特征维对应坐标轴x,y；样本图形标记及大小
        plt.plot(dataSet[i,0],dataSet[i,1],marksamples[markindex],markersize=6)

    #绘中心点
    markcentroids=['dr','db','dg','dk','^b','sk','<r']#聚类中心图形标记
    for i in range(k):
        plt.plot(centroids[i,0],centroids[i,1],markcentroids[i],markersize=15)

    plt.title('k-means cluster result') #标题
    plt.show()


def kMeans(dataSet, k, distMeas=disEclud, createCent=randCent):
    '''
    k-均值聚类算法
    :param dataSet: 数据集
    :param k:簇的数目
    :param distMeas:计算距离的函数（可选）
    :param createCent:创建初始质心的函数（可选）
    :return:
    '''
    # shape获取几行几列的矩阵 返回 (m,n)
    m = shape(dataSet)[0]
    # 簇分配结果矩阵 有两列[簇索引值，误差] 误差是指当前点到簇质心的距离
    clusterAssment = mat(zeros((m, 2)))
    # 创建k个簇质心
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False

        # 分别标记每个点最近的质心
        for i in range(m):
            minDist = inf   # 正无穷大
            minIndex = -1
            for j in range(k):
                # 计算1个点到每个质心的距离
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                # 取出最小的距离的点，和质心的索引
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:  # while循环两遍，第二遍做校验
                clusterChanged = True
            # 存储每个点对应得质心索引和误差
            clusterAssment[i, :] = minIndex, minDist ** 2  # ** 表示乘方
        print 'centroids=', centroids

        # 循环质心，更新质心位置
        for cent in range(k):
            # 取出按质心分类的点
            # print 'clusterAssment[:, 0].A==',clusterAssment[:, 0].A
            # clusterAssment[:, 0].A== [[ 3.] [ 2.][ 5.] ....]
            # print 'nonzero(clusterAssment[:, 0].A == cent)==', nonzero(clusterAssment[:, 0].A == cent)
            # nonzero(clusterAssment[:, 0].A == cent)== (array([ 2, 14, 20, 38, 44, 47, 50, 53, 59]), array([0, 0, 0, 0, 0, 0, 0, 0, 0]))
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            # 按列计算平均值
            centroids[cent, :] = mean(ptsInClust, axis=0)
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

        newCentList = []
        for i in range(len(centList)):
            newCentList.append(centList[i].tolist()[0])
        newCentList = mat(newCentList)
    return newCentList, clusterAssment

if __name__ == '__main__':
    dataMat = loadDateSet('testSet2.txt')
    '''
    print dataMat

    print min(dataMat[:, 0])
    print max(dataMat[:, 0])
    print min(dataMat[:, 1])
    print max(dataMat[:, 1])
    '''
    print randCent(dataMat, 2)


    print disEclud(dataMat[0], dataMat[1])

    # k-均值聚类算法
    # centroids, clusterAssment = kMeans(dataMat, 4)
    # datashow(dataMat, 4, centroids, clusterAssment)
    # 二分k-均值聚类算法
    centroids2, clusterAssment2 = biKmeans(dataMat, 3)
    datashow(dataMat, 3, centroids2, clusterAssment2)