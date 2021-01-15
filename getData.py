#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 需要安装程序
# 1. git
# 2. vscode编辑器（或者 notePad++）
# 3. pip
# 4. python 3.8

import requests
import tablib
from lxml import etree
from xlrd import open_workbook
from xlutils.copy import copy
import time
import translate_image_to_text as formatImg
from PIL import Image
from io import BytesIO
from urllib.request import urlretrieve
import pdb

# 下载图片的方法
def urllib_download(image_url):
    # urlretrieve(image_url, './current.png')

    r = requests.get(image_url)

    with open('./current.png', 'wb') as f:
        f.write(r.content)

# 获取每个单元格的数据函数
def getTdValue (ele, index):
    path = './td[{index}]/text()'
    value = ele.xpath(path.format(index=index))
    valueStr = ''.join(value).replace('\n', '')

    return valueStr.strip() if valueStr else '无'

def getCodeText (imgUrl):

    urllib_download(imgUrl)
    imgLocalPath = './current.png'

    # 获取验证码的值
    return formatImg.getImgCode(imgLocalPath)

def getRowsData(name, targetUrl, headers, imgUrl):
    """
    docstring
    """

    # 毫秒级时间戳
    timeText = int(round(time.time() * 1000))

    imgUrl = 'http://jpxb.bjmu.edu.cn/JournalX_jpxb/kaptcha.jpg?d_a_={0}'.format(timeText)

    # 获取验证码的值
    codeText = getCodeText(imgUrl)

    print('这边获取到的验证码：', codeText)

    # 请求参数构建
    form_data={
        'personSearch.name': name,
        'personSearch.rolsesp': 3,
        'randomCode': codeText
    }

    # 发出数据请求
    res=s.post(targetUrl,data=form_data,headers=headers)
    
    # 将请求返回的结果存储到txt文件中
    with open('G:/development/project/spider-python/test.txt', 'w', encoding='utf-8') as f:
        f.write(res.text)

    html=etree.HTML(res.text)
    rows=html.xpath('//table[@class="list"]/tr') 
    tr_id=html.xpath('//tr[@id="register_error"]/td//text()')

    return rows, bool(tr_id)


# 追加数据到表格里面（已有的表格）
def appendDataToExcel (currentData):

    excelPath = 'G:/development/project/spider-python/test.xls'

    # 用 xlrd 提供的方法读取一个excel文件
    rexcel = open_workbook(excelPath,formatting_info=True) # 保留原有样式
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
    excel.save(excelPath) # xlwt 对象的保存方法，这时便覆盖掉了原来的 Excel

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Host': 'jpxb.bjmu.edu.cn',
    'Cookie': 'author_user_id=66ODkWxkjOrriypleJCEK7gg900D; author_password_id=; JSESSIONID=FD775BCF8671DC59C5709F0DD5CBB784; JSESSIONID=9784AA12E25EC4C60F4CD2962F50F496'
}

# 登陆的地址
url_login = 'http://jpxb.bjmu.edu.cn/JournalX_jpxb/Login.action'


# 建立一个session层
s = requests.Session() 


if __name__ == '__main__':

    imgUrl = 'http://jpxb.bjmu.edu.cn/JournalX_jpxb/kaptcha.jpg'
    loginCodeText = getCodeText(imgUrl)

    print('登陆页面的验证码： ', loginCodeText)

    
    # 登陆需要的参数
    login_data={
        'j_username': 'AAA117340102F7347E8E4D27C9F831D2___1___author___jaiimjlsuan',
        'j_password': 'D5442E7F1547E44407E77A6C4E705E94BB0F874C48AB3F19',
        'j_randomCode': loginCodeText
    }
    
    # login 
    r = s.post(url_login, data=login_data, headers=headers)
    print("登陆成功：", r.status_code)

    # 如果登陆失败了直接退出
    if (r.status_code is not 200):
        exit()

    # 获取名字列表
    nameList = []
    with open('G:/development/project/spider-python/full_name.txt', 'r', encoding='utf-8') as nameText:
            nameList = nameText.readlines()

    # 目标的url地址
    targetUrl='http://jpxb.bjmu.edu.cn/JournalX_jpxb/author/Contribution!searchAuthors.action?id=6159860102&flag=0&processId=1159860001&comm=0'

    # 根据名字查询对应的内容
    for name in nameList:
        print('当前查询的人:', name)

        rows = None
        for count in range(3):

            rows, ret = getRowsData(name, targetUrl, headers, imgUrl)

            if not ret:
                break
        else:
            print("三次还是错的。。。。")
            continue

        if rows:
            # 把数据存储到表格里面
            print("有输出： {}".format(rows))
            appendDataToExcel(rows[1:])
        else:
            print("gg")
