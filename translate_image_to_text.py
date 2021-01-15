#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# import pytesseract
from PIL import Image
import requests
import base64

'''
数字识别
'''

# 获取 access_token
# encoding:utf-8
# client_id 为官网获取的AK， client_secret 为官网获取的SK
# access_token: 要获取的Access Token；
# expires_in： Access Token的有效期(秒为单位，一般为1个月)；
# error： 错误码；关于错误码的详细信息请参考下方鉴权认证错误码。
# error_description： 错误描述信息，帮助理解和解决发生的错误。
def getAccessToken(apiKey, secretKey):

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ apiKey +'&client_secret='+ secretKey
    response = requests.get(host)
    token = ''

    if response:
        result = response.json()
        # print('获取验证码的结果json:', result)
        if result['access_token']:
            token = result['access_token']

    return token



def getImgCode (img):

    # 图片路径
    img_path = img

    # 验证码请求地址
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/numbers"
    API_KEY = '1t4uGIX9Tfik4pCkEtdPcLG9'
    SECRET_KEY = 'CkGt6e7jd7MB47AbtozWiS6CUTddhdnD'

    # 二进制方式打开图片文件
    f = open(img_path, 'rb')
    img = base64.b64encode(f.read())

    params = {"image":img}
    accessToken = getAccessToken(API_KEY, SECRET_KEY)

    if len(accessToken) == 0:
        print('获取token失败！')
        exit()

    request_url = request_url + "?access_token=" + accessToken
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    codeJson = '验证码识别失败-默认值'

    if response:
        codeJson = response.json()
        wordsResult = codeJson['words_result']
        codeText = wordsResult[0]['words']

    return codeText

# if __name__ == '__main__':

#     imgPath = './kaptcha.jpg'

#     codeNum = getImgCode(imgPath)

#     print('这边获取到的验证码：', codeNum)