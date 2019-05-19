#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import copy
import math
import xlrd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# 读入数据
def read_data():
    fname = r'C:\Users\HP\Desktop\Dataset.xlsx'
    filename = xlrd.open_workbook(fname)
    sheet = filename.sheets()[0]
    label = np.zeros((178, 1))
    data = np.zeros((178, 13))
    for i in range(3, 181):
        row_data = sheet.row_values(i)
        l = np.array(row_data[0])
        d = np.array(row_data[1:])
        label[i-3, 0] = l
        data[i-3, :] = d
    data = MinMaxScaler().fit_transform(data)       # 将数据归一化
    return label, data                              # label存的是已聚类的类别(answer) , data存的是13维的数据


# 层次聚类(平均距离)
def hierarchical_clustering(label, data, k):
    clust = []
    for i in range(178):
        clust.append([i])
    print(clust)
    num_clust = len(clust)
    while num_clust > k:
        # distance = np.zeros(num_clust,num_clust)  # distance用来存每两个类别之间的距离
        min_dis = 10000000
        min_x = -1
        min_y = -1
        for i in range(num_clust):
            for j in range(i+1, num_clust):
                # distance[i, j] = distance_ave(clust[i], clust[j], data)
                # distance[j, i] = diatance[i,j]
                dis = distance_ave(clust[i], clust[j], data)
                if dis < min_dis:
                    min_dis = dis
                    min_x = i
                    min_y = j
        clust[min_x].extend(clust[min_y])
        del clust[min_y]
        num_clust=len(clust)
    print(clust)


def k_means(label, data, k):
    list_rand = []
    for i in range(k):
        while 1:
            randx = math.floor(np.random.rand(1) * 177)
            for j in range(len(list_rand)):
                if list_rand[j] == randx:
                    continue
            list_rand.append(randx)
            break
    list_1 = np.array([data[list_rand[0]], data[list_rand[1]], data[list_rand[2]]])
    list_2 = np.zeros((3, 13))
    num_of_times = 0
    while ~((list_1 == list_2).all()):
        list_2 = copy.deepcopy(list_1)

        clust = []
        for i in range(k):
            clust.append([])

        for i in range(178):
            dis = []
            for j in range(k):
                dis.append(distance_chebyshev(data[i], list_1[j]).tolist())
            index = dis.index(min(dis))
            clust[index].append(i)
        for i in range(k):
            sum_of_clust = np.zeros((1, 13))
            for j in clust[i]:
                sum_of_clust += data[j]
            if len(clust[i]) != 0:
                list_1[i] = sum_of_clust / len(clust[i])
            else:
                list_1[i] = np.array([0])
        num_of_times += 1
    print(clust)




def distance_ave(clust_1, clust_2, data):
    dis = 0
    for i in range(len(clust_1)):
        for j in range(len(clust_2)):
            dis = dis + distance_chebyshev(data[i], data[j])
    dis = dis / (len(clust_1) * (len(clust_2)))
    return dis


def distance_euclid(a, b):
    return np.sqrt(np.sum((a-b)**2))


def distance_manhattan(a, b):
    return np.sum(abs(a-b)**2)


def distance_chebyshev(a, b):
    return np.max(abs(a-b))


if __name__ == '__main__':
    label, data = read_data()
    # hierarchical_clustering(label, data, 3)
    k_means(label, data, 3)

