# train2database
"""
爬取火车数据写入数据库
写的python小程序
仅供学习使用

默认建表代码
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
