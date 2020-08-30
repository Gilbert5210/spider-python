#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# import pytesseract
from PIL import Image
import pytesseract as pt

#新建Image对象
image = Image.open("img-code.jpg")

#进行置灰处理
image = image.convert('L')

#这个是二值化阈值
threshold = 150   
table = []

for i in  range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
#通过表格转换成二进制图片，1的作用是白色，不然就全部黑色了
image = image.point(table,"1")
image.show()

# 调用 pytesseract 识别图片文字
text = pt.image_to_string(image)
# result = tesserocr.image_to_text(image)

print('验证码：', text)