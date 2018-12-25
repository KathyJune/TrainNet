# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import copy
import node as nd
import pickle


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

# nodes = {}
# for sec in secs:
#     f_station = sec.split('-')[0]
#     t_station = sec.split('-')[1]
#     if not (f_station in nodes):
#         nodes[f_station] = {}
#     if not (t_station in nodes):
#         nodes[t_station] = {}
#     for dis in secs[sec]:
#         nodes[f_station][t_station] = dis
#         nodes[t_station][f_station] = dis

# ps = nd.PathSolve()
# ps.nodes = nodes
# seps = []
# for node in nodes:
#     for link_node in nodes[node]:
#         if int(link_node) > int(node):
#             ps.solve(str(node), None, str(node), str(link_node))
#             if len(ps.paths) > 1:
#                 a = []
#                 for p in ps.paths:
#                     if len(p[0]) == 2:
#                         dis = p[1]
#                     else:
#                         a.append(p[1])
#                 for i in range(len(a)):
#                     if a[i] == dis:
#                         seps.append([node, link_node])
#             ps.paths = []
# for s in seps:
#     del ps.nodes[s[0]][s[1]]
# ps.paths = []
# length = 0
# for node in nodes:
#     for link_node in nodes[node]:
#         length += nodes[node][link_node]
# print(length / 2)
# file = open('data/#z#y#d', 'wb')
# pickle.dump([length / 2, zongchang], file)
