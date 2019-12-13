# -*- coding:utf-8 -*-
# @Time    :2019/12/10 0010 16:34
# @Author  :wulin
# @Mail    :286075568@qq.com
# @FileName: test.py
# @Software: PyCharm
import requests

# url="https://api.t.iwubida.com/api/buyer/platform/seller/market/page?page=0&size=10"
# headers = {
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/json;charset=UTF-8',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
#     'authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJtb2R1bGUiOiJidXllckNvbnRleHQiLCJidXllckNvbnRleHQiOiJ7XCJidXllcklkXCI6ODQxfSIsImV4cCI6MTU3NjE4MTA4NX0.3wOiIm7J4XhqdJdwyJWHTw5ph2OE0sHptW0zBxzEaIM',
#
# }
# payload ={"comment":"AFSAF","requestId":"355"}
#
# # r = requests.post(url, json=payload, headers=headers,verify=False)
# r=requests.get(url,headers=headers)
# print(r)
# from common.http_request import HTTP
# from Unittest import datadriven
#
# http = HTTP(datadriven.writer)
# url = "https://api.t.iwubida.com/api/buyer/platform/seller/market/page?"
# pa = "page=0&size=10"
# http.addheader('authorization',
#                'eyJhbGciOiJIUzI1NiJ9.eyJtb2R1bGUiOiJidXllckNvbnRleHQiLCJidXllckNvbnRleHQiOiJ7XCJidXllcklkXCI6ODQxfSIsImV4cCI6MTU3NjE4MTA4NX0.3wOiIm7J4XhqdJdwyJWHTw5ph2OE0sHptW0zBxzEaIM')
# res=http.get(url, params=pa)
# print(res)

import pymysql

conn = pymysql.connect(host='192.168.1.246', port=3306, user='ydh_test', password='ydh_test_123',
                       database='ydh_test', charset='utf8')
cur = conn.cursor()

SQL1 = "SELECT id ,buyer_id FROM ydh_buyer_request WHERE contact_phone ='13400000145' AND status='processing' AND seller_id='2';"

cur.execute(SQL1)
conn.commit()
# 获取所有记录列表
results = cur.fetchall()
print(results)

for row in results:
    id = row[0]
    nickname = row[1]

    # 打印结果
    print("id=%s,nickname=%s" % (id, nickname))

