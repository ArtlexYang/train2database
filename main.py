# -*- coding: utf-8 -*-
# @Author  : ArtlexKylin

"""
表内容
create table TRAIN_TOTAL(
    TID varchar(20) default '0' not null,  -- 车次
    START_TIME datetime default '2020-07-01 00:00:00' not null,  -- 出发时间
    ARRIVE_TIME datetime default '2020-07-01 00:00:00' not null,  -- 到达时间
    RUN_TIME int default 0 not null,  -- 行驶时间
    FROM_STATION varchar(20) default '空' not null,  -- 出发城市
    TO_STATION varchar(20) default '空' not null,  -- 到达城市
    SEAT_TYPE varchar(20) default '二等座' not null,  -- 座位类型
    TICKETS_LEFT int default 100 not null,  -- 余票
    TICKET_PRICE double(10,2) default 100 not null,  -- 票价
    constraint train_total_pk primary key(TID,START_TIME,ARRIVE_TIME,FROM_STATION,TO_STATION,SEAT_TYPE)  -- 主键
);
"""

"""本程序出于学习目的编写"""

import optStation, optData

if __name__ == "__main__":
    # 自定初值
    place_name=['北京', '上海', '广州', '深圳']  # 想要爬取的地名（包含该地所有车站）
    date='2020-07-01'  # 爬取的日期，只能从今天往后一个月内
    host = 'localhost'  # 数据库ip
    port = 3306  # 数据库端口
    user = 'root'  # 数据库用户名
    passwd = '123456'  # 数据库用户名对应密码
    db = 'train'  # 数据库名
    table_name = 'train_total'  # 数据库表名

    # 获取需要数据写入excel
    print('开始获取数据')
    # 获取 车站及缩写 字典
    station_name, name_station = optStation.readStation()  # （已经读好）

    # 获取四个城市之间来往火车信息
    for i in place_name:
        for j in place_name:
            if i == j:  # 出发站和终点站不能一致
                continue
            optData.getData(station_name, i, j, date)
    print('获取数据完成')

    # 合并excel，规范日期格式
    print('开始合并')
    print('开始规范日期格式')
    # 合并数据
    optData.totalData(place_name, date)
    print('规范完成')
    print('合并完成')

    # 写入数据库
    print('开始写入数据库')
    optData.excelTOsql(host, port, user, passwd, db, table_name)
    print('数据库写入完成')