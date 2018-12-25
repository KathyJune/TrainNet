# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import copy
import node as nd
import pickle
import djk


# temp_nw=pd.read_excel(path+'150103lc.xls')
temp_nw = pd.read_excel('data/120523_encoded.xls')
# 999 nodes 3941 links
temp_nw.cc = temp_nw.cc.astype('str')

trains_uniq = np.unique(np.array(temp_nw['cc'], dtype=str))
print(len(trains_uniq))

zhan_licheng_che = []  # 组织三段模型[车次号,车站s，里程s]
for train in trains_uniq:
    checi_new = temp_nw[temp_nw['cc'] == str(train)]
    chezhans = list(checi_new['cz'])
    lichengs = list(checi_new['lc'])
    chunk = [chezhans, lichengs, train]
    zhan_licheng_che.append(chunk)

print('三段模型组织好了')

luxian = {}  # 去重的临近车站对
for unit in zhan_licheng_che:
    chezhans = unit[0]
    lichengs = unit[1]
    che = unit[2]
    if re.search('[zZ]', unit[2]):
        continue
    for i in range(len(chezhans) - 1):
        chezhan1 = str(chezhans[i])
        chezhan2 = str(chezhans[i + 1])
        juli = abs(int(lichengs[i + 1]) - int(lichengs[i]))
        zuhe1 = chezhan1 + '-' + chezhan2
        zuhe2 = chezhan2 + '-' + chezhan1
        if zuhe1 in luxian:
            if juli in luxian[zuhe1]:
                #                 print(zuhe1,juli)
                continue
            else:
                luxian[zuhe1].append(juli)
        else:
            if zuhe2 in luxian:
                if juli in luxian[zuhe2]:
                    continue
                else:
                    luxian[zuhe2].append(juli)
            else:
                luxian[zuhe1] = [juli]

xiaoduan = copy.deepcopy(luxian)  # 用深拷贝新建对象
for chezhans in luxian:
    if chezhans == '124-15':
        aa = 1
    dajulis = luxian[chezhans]
    for dajuli in dajulis:
        chezhan1 = int(chezhans.split('-')[0])
        chezhan2 = int(chezhans.split('-')[1])
        for xianlu in zhan_licheng_che:
            if chezhan1 in xianlu[0] and chezhan2 in xianlu[0]:
                index_chezhan1 = xianlu[0].index(chezhan1)
                index_chezhan2 = xianlu[0].index(chezhan2)
                if abs(index_chezhan1 - index_chezhan2) > 1:
                    #                 print(chezhan1,chezhan2)
                    dajuli2 = abs(
                        xianlu[1][index_chezhan1] - xianlu[1][index_chezhan2])
                    if dajuli2 == dajuli:  # 证明并不是小段，而是大距离
                        if dajuli in xiaoduan[chezhans]:
                            #                             print('000')
                            xiaoduan[chezhans].remove(dajuli)  # 这时把大距离提出

zongchang1 = 0
for chezhans in luxian:
    for chang in luxian[chezhans]:
        zongchang1 += chang
print(zongchang1)

zongchang = 0
print("number of sections")
print(len(xiaoduan))
for chezhans in xiaoduan:
    ndis = len(xiaoduan[chezhans])
    if ndis > 1:
        print(xiaoduan[chezhans])
    for chang in xiaoduan[chezhans]:
        zongchang += chang
print(zongchang)
secs = xiaoduan

# cutting line: above is wrtten by wbz, below is written by kathy
# ------------------***************-----------------
sections = xiaoduan
# ------------------***************-----------------

edges = []
for sec in secs:
    f_station = sec.split('-')[0]
    t_station = sec.split('-')[1]
    for dis in secs[sec]:
        edges.append((int(f_station), int(t_station), dis))
        edges.append((int(t_station), int(f_station), dis))
# deep copy
# edges_cp = copy.copy(edges)
count = 0
while count != len(edges):
    # print('here')
    edge = edges[count]
    count += 1
    # print(count)
    edges_to_remove = []
    edges_cp = copy.copy(edges)
    sym_edge = (edge[1], edge[0], edge[2])
    edges_to_remove.append(sym_edge)
    edges_to_remove.append(edge)
    length = 0
    while length < edge[2]:
        for i in edges_to_remove:
            edges_cp.remove(i)
        edges_to_remove = []
        length, path = djk.dijkstra(edges_cp, edge[0], edge[1])
        if path == []:
            break
        # print(path)
        if length > edge[2]:
            # print('>')
            continue
        elif length == edge[2]:
            print('=')
            print("original pair", edge, "path", path)
            edges.remove(edge)
            edges.remove(sym_edge)
            count -= 1
        else:
            # print('<')
            for j in path:
                edges_to_remove.append((j[0], j[1], j[2]))
                edges_to_remove.append((j[1], j[0], j[2]))
        

total_length = 0
for edge in edges:
    total_length += edge[2]

print("the total length")
print(total_length / 2)
