# -*- coding: utf-8 -*-
# @Author  : ArtlexKylin

# 用来获取车站及其缩写，写入文件
def writeStation():
    file_path='station.txt'
    f=open(file_path,'r',encoding='utf-8')
    lines=f.readlines()
    f.close()
    all=''
    for i in lines:
        all = all + i
    areas = all.split('@')
    length=len(areas)
    station_name={}
    for i in range(1,length):
        tmps = areas[i].split('|')
        station_name[tmps[1]] = tmps[2]
    f1=open('station.txt','a+',encoding='utf-8')
    for data in station_name:
        f1.write(data+' '+station_name[data]+'\n')
    f1.close()

# 从文件中读取车站及其缩写
def readStation():
    station_name = {}
    name_station = {}
    f = open('station.txt', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for i in lines:
        temps = i.split(' ')
        station_name[temps[0]] = temps[1][:-1]  # 从站名找到对应字母
        name_station[temps[1][:-1]] = temps[0]  # 从字母找到对应站名
    return station_name, name_station