# -*- coding: utf-8 -*-
# @Author  : ArtlexKylin

import pymysql
import requests
import json
import xlrd
import xlwt

# header如果拒绝访问，可以改为自己的
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    "Cookie": 'RAIL_EXPIRATION=1591512512449; RAIL_DEVICEID=TbK2nQu7QNjdlj8nwm4awJo5UHaT29WtLbtF17p4_zbFE-k9Vk7YvMI1zPMuPUc_pStJ1UuNMKgGdv8kqAWH8CsZ2w93vZOsDHn1qOggI2JSKd0zjWBUbfU9S0slgSb67Kpiv0jThVR7ZXyplERhP1pl2w_sh-2l; BIGipServerpool_index=753926666.43286.0000; route=495c805987d0f5c8c84b14f60212447d; BIGipServerotn=602931722.24610.0000'
}


def getData(station_name, fromName, toName, startDate):
    """使用接口查询火车信息，时间不能早于当前日期

    :param station_name:站台名
    :param fromName:出发地名
    :param toName:到达地名
    :param startDate:出发日期
    :return:
    """

    if fromName not in station_name:
        print('当前系统无此出发站')
    if toName not in station_name:
        print('当前系统无此终点站')

    # api连接
    url = 'https://i.meituan.com/uts/train/train/querytripnew?fromPC=1' \
          '&train_source=meituanpc@wap&uuid=a2bab8b38b364d7f8d7a.1590661315.1.0.0' \
          '&from_station_telecode={}&to_station_telecode={}&yupiaoThreshold=0&start_date={}' \
          '&isStudentBuying=false'.format(station_name[fromName], station_name[toName], startDate)

    response = requests.get(url, headers=headers).json()

    # 写入excel
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')

    # 创建一个worksheet
    worksheet = workbook.add_sheet('Sheet1')

    # 写入excel
    # full_train_code:车次;
    # start_time:出发时间; arrive_time:到达时间; run_time:运行时间;
    # from_station_name:出发站; to_station_name:终点站;
    # seats座位信息; seat_type_name:座位类型; seat_min_price:座位金额; seat_yupiao:座位余票
    row = 0
    for train in response['data']['trains']:
        for seats in train['seats']:
            # 参数对应 行, 列, 值
            worksheet.write(row, 0, label=train['full_train_code'])  # 车次
            worksheet.write(row, 1, label=train['start_time'])  # 出发时间
            worksheet.write(row, 2, label=train['arrive_time'])  # 到达时间
            worksheet.write(row, 3, label=train['run_time_minute'])  # 运行时间（分钟）
            worksheet.write(row, 4, train['from_station_name'])  # 出发站
            worksheet.write(row, 5, train['to_station_name'])  # 终点站

            # 顺便把座位信息拆开
            worksheet.write(row, 6, label=seats['seat_type_name'])  # 座位类型
            worksheet.write(row, 7, label=seats['seat_min_price'])  # 最低价格
            worksheet.write(row, 8, label=seats['seat_yupiao'])  # 余票
            worksheet.write(row, 9, label=seats['supportCandidate'])  # 是否支持预约

            row += 1  # 行加一

    # 将主要数据保存
    workbook.save(fromName + '_' + toName + '.xls')

    # 将所有数据保存
    with open(fromName + '_' + toName + '.json', "w", encoding="utf-8") as f:
        json.dump(response, f, ensure_ascii=False)  #　ensure_ascii=False防止将中文转换成十六进制字符


def totalData(place_name, date):
    """将各个分表整合成一个大表

    :param place_name:地点列表
    :param date:爬取日期'year-moth-day'
    :return:无
    """

    # 配置写操作参数
    writeExcel = xlwt.Workbook(encoding='utf-8')
    writeTable = writeExcel.add_sheet('Sheet1')
    writeRow = 0
    for fromName in place_name:
        for toName in place_name:
            if fromName == toName:  # 出发站和终点站不能一致
                continue
                # 配置读操作参数
            readExcel = xlrd.open_workbook(fromName + '_' + toName + '.xls')
            readTable = readExcel.sheet_by_name("Sheet1")
            rowNum = readTable.nrows
            colNum = readTable.ncols

            # 遍历读文件
            for i in range(rowNum):
                # 对时间进行处理（有些时间是没有秒的）%H:%M:%S
                start_time = readTable.cell(i, 1).value
                # print(start_time)
                if type(start_time) is not float:
                    # print(type(start_time))
                    start_time += ':00'
                    start_time = date + ' ' + start_time
                    writeTable.write(writeRow, 1, label=start_time)
                else:
                    writeTable.write(writeRow, 1, label=date + ' ' + str(
                        xlrd.xldate.xldate_as_datetime(readTable.cell(i, 1).value, 0).__format__('%H:%M:%S')))

                arrive_time = readTable.cell(i, 2).value
                if type(arrive_time) is not float:
                    arrive_time += ':00'
                    arrive_time = date + ' ' + arrive_time
                    writeTable.write(writeRow, 2, label=arrive_time)
                else:
                    writeTable.write(writeRow, 2, label=date + ' ' + str(
                        xlrd.xldate.xldate_as_datetime(readTable.cell(i, 2).value, 0).__format__('%H:%M:%S')))

                # 写入保存文件
                writeTable.write(writeRow, 0, label=readTable.cell(i, 0).value)  # 第i行已经不是原来的TID了

                writeTable.write(writeRow, 3, label=readTable.cell(i, 3).value)
                writeTable.write(writeRow, 4, label=readTable.cell(i, 4).value)
                writeTable.write(writeRow, 5, label=readTable.cell(i, 5).value)
                writeTable.write(writeRow, 6, label=readTable.cell(i, 6).value)
                writeTable.write(writeRow, 7, label=readTable.cell(i, 7).value)
                writeTable.write(writeRow, 8, label=readTable.cell(i, 8).value)
                writeTable.write(writeRow, 9, label=readTable.cell(i, 9).value)

                writeRow += 1
    writeExcel.save('total.xls')
    return 1


def excelTOsql(host, port, user, passwd, db, table_name):
    """将表数据写入数据库

    :param host:数据库ip
    :param port:数据库端口
    :param user:数据库用户名
    :param passwd:数据库用户名对应密码
    :param db:数据库名
    :param table_name:数据库表名
    :return:无
    """

    # 配置读操作参数
    readExcel = xlrd.open_workbook("total.xls")
    readTable = readExcel.sheet_by_name("Sheet1")
    rowNum = readTable.nrows
    colNum = readTable.ncols

    # 连接数据库
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)  # 建立连接
    cur = conn.cursor()  # 获取游标

    for i in range(rowNum):
        # 获取数据
        tid = str(readTable.cell(i, 0).value)  # 当前行的TID
        # 转换纯数字车次
        if '.' in tid:
            tid = tid.split('.')[0]
        start_time = readTable.cell(i, 1).value
        arrive_time = readTable.cell(i, 2).value
        run_time = int(readTable.cell(i, 3).value)
        from_station = readTable.cell(i, 4).value
        to_station = readTable.cell(i, 5).value
        seat_type = str(readTable.cell(i, 6).value)
        tickets_left = int(readTable.cell(i, 7).value)
        ticket_price = float(readTable.cell(i, 8).value)

        # 插入数据库
        sql = 'INSERT INTO ' + table_name + """(
                TID,START_TIME,ARRIVE_TIME,RUN_TIME,FROM_STATION,TO_STATION,SEAT_TYPE,TICKETS_LEFT,TICKET_PRICE)
                 VALUES ('%s', '%s', '%s', %s, '%s', '%s', '%s', %s, %s);""" % \
              (tid, start_time, arrive_time, run_time, from_station, to_station, seat_type, tickets_left, ticket_price)
        # print(sql)
        try:
            # 执行sql语句
            cur.execute(sql)
            # 提交到数据库执行
            conn.commit()
        except:
            # 遇到错误回滚
            conn.rollback()
            print(sql)
            print('插入数据错误')

    conn.close()  # 关闭数据库连接