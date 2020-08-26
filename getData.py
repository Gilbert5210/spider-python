#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
import tablib
from lxml import etree
from xlrd import open_workbook
from xlutils.copy import copy

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Host': 'www.zhzdxzz.com',
    'Cookie': 'JSESSIONID=F0DE178607C873DC9A5D2572CE9CE359; author_user_id=zbRdkWOYjOhiiyHRNaeWbpfHi6zDhvLL; author_password_id=; JSESSIONID=1C1681627B9D36CED53E85CF0017EF0E; _gscu_1674708056=984473645srw1b20; _gscbrs_1674708056=1; _gscs_1674708056=9844736452x3m720|pv:1'
}

url_login = 'http://www.zhzdxzz.com/journalx/Login.action'
login_data={
    # 'j_magazine': 1,
    # 'username': 'admin123',
    # 'j_username': 'admin123___1___author',
    # 'j_password': 'admin123',
    # 'j_role': 'author',
    # 'person.email': '',
    # 'person.rolsesp': 6,

    'j_username': 'B0A901BB6C8C999DE0768F1DB508A586___1___author___jaiimjlsuan',
    'j_password': 'D5442E7F1547E4445F41235539F35D18',
    'j_role': 'author',
    'person.email': '',
    'person.rolsesp': 3
}

# 建立一个session层
s = requests.Session() 

# login 
r = s.post(url_login, data=login_data, headers=headers)
print("登陆成功：", r.status_code)

# 获取名字列表
nameList = []
with open('g:/Gilbert/project/name.txt', 'r', encoding='utf-8') as nameText:
        nameList = nameText.readlines()

# print('名字列表:', nameList)
# exit()

# 目标的url地址
url='http://www.zhzdxzz.com/journalx/author/Contribution!searchAuthors.action?id=3166875708&flag=0&processId=1166867001&comm=0'
#url='http://www.zggrkz.com/journalx_grkz/author/Author!incompletion.action'


# 获取每个单元格的数据函数
def getTdValue (ele, index):
    path = './td[{index}]/text()'
    value = ele.xpath(path.format(index=index))
    valueStr = ''.join(value).replace('\n', '')

    return valueStr.strip() if valueStr else '无'

# 追加数据到表格里面（已有的表格）
def appendDataToExcel (currentData):
    # 用 xlrd 提供的方法读取一个excel文件
    rexcel = open_workbook("g:/Gilbert/project/current.xls",formatting_info=True) # 保留原有样式
    # 用 xlrd 提供的方法获得现在已有的行数
    rows = rexcel.sheets()[0].nrows 
    # 用 xlutils 提供的copy方法将 xlrd 的对象转化为 xlwt 的对象
    excel = copy(rexcel) 
    # 用 xlwt 对象的方法获得要操作的 sheet
    table = excel.get_sheet(0) 
    row = rows


    for ele in currentData:
        
        # xlwt对象的写方法，参数分别是行、列、值
        table.write(row, 0, getTdValue(ele, 2)) 
        table.write(row, 1, getTdValue(ele, 3)) 
        table.write(row, 2, getTdValue(ele, 4)) 
        table.write(row, 3, getTdValue(ele, 5)) 
        table.write(row, 4, getTdValue(ele, 6)) 
        table.write(row, 5, getTdValue(ele, 7)) 
        table.write(row, 6, getTdValue(ele, 8)) 
        table.write(row, 7, getTdValue(ele, 9)) 
        table.write(row, 8, getTdValue(ele, 10)) 
        table.write(row, 9, getTdValue(ele, 11)) 
        table.write(row, 10, getTdValue(ele, 12)) 
    
        row += 1
    excel.save("g:/Gilbert/project/current.xls") # xlwt 对象的保存方法，这时便覆盖掉了原来的 Excel

# 根据名字查询对应的内容
for name in nameList:

    print('当前查询的人:', name)

    # 请求参数构建
    form_data={
        'personSearch.name': name,
        'personSearch.rolsesp': 3
    }

    # 发出数据请求
    res=s.post(url,data=form_data,headers=headers)
    
    # 将请求返回的结果存储到txt文件中
    # with open('g:/Gilbert/test.txt', 'w', encoding='utf-8') as f:
    #     f.write(res.text)

    html=etree.HTML(res.text)
    rows=html.xpath('//table[@class="list"]/tr')

    if not rows:
        continue
    appendDataToExcel(rows[1:])

# print('最终结果：', resultData)


# if resultData:
#     headers = tuple([key for key in resultData[0].keys()])
#     realData = []

#     for item in resultData:
#         body = []
#         for v in item.values():
#             body.append(v)
#         realData.append(tuple(body))

#     excelData = tablib.Dataset(*realData, headers=headers)
#     open('中国医药工业杂志.xlsx', 'wb').write(excelData.xlsx)