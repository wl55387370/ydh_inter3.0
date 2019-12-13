# -*- coding: utf-8 -*-
# @Time    : 2019/11/18  下午 11:44
# @Author  : wulin
# @Email   : 286075568@qq.com
# @FileName: http_request.py
# @Software: PyCharm


import requests, json, traceback, jsonpath, time, datetime
from common.outlog import MyLog
import pymysql
from common.mysql import Mysql

logger = MyLog('INFO')


class HTTP:

    def __init__(self, writer):
        requests.packages.urllib3.disable_warnings()
        self.session = requests.session()
        self.session.headers['content-type'] = 'application/x-www-form-urlencoded'
        self.session.headers[
            'user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        self.result = ''
        self.jsonres = {}
        self.params = {}
        self.url = ''
        self.writer = writer

    def seturl(self, u):

        if u.startswith('http') or u.startswith('https'):
            self.url = u
            self.writer.write(self.writer.row + 1, 8, 'PASS')

        else:
            logger.error('error：url格式错误')
            self.writer.write(self.writer.row + 1, 8, 'FAIL')

    def post(self, url, d=None, j=None):

        if not (url.startswith('http') or url.startswith('https')):
            url = self.url + '/' + url

        if j is None or j == '':
            pass
        else:
            j = j.encode('utf-8')

        d = self.__get_param(d)
        if d is None or d == '':
            pass
        elif d.startswith('{'):
            d = d.encode('utf-8')
            self.session.headers['content-type'] = 'application/json'
        else:
            d = self.__get_param(d)

            d = self.__get_data(d)

            self.session.headers['content-type'] = 'application/x-www-form-urlencoded'

        res = self.session.post(url, d, j, verify=False)

        self.result = res.content.decode('UTF-8')
        logger.info(self.result)
        try:
            # self.jsonres = json.loads(self.result)
            jsons = self.result
            jsons = jsons[jsons.find('{'):jsons.rfind('}') + 1]
            self.jsonres = json.loads(jsons)
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            print(self.jsonres)
            return True

        except Exception as e:
            # 异常处理的时候，分析逻辑问题
            logger.error('error：请求错误！')
            logger.exception(e)
            self.jsonres = {}

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    def get(self, url, params=None):

        if not (url.startswith('http') or url.startswith('https')):
            params = self.__get_param(params)
            url = self.url + '/' + url + "?" + params
            print(url)
        else:
            params = self.__get_param(params)
            print(params)
            url = url + "?" + params
            print(url)

        # 如果请求https请求，报ssl错误，就添加verify=False参数
        res = self.session.get(url, verify=False)
        self.result = res.content.decode('utf8')
        logger.info(self.result)
        try:
            jsons = self.result
            jsons = jsons[jsons.find('{'):jsons.rfind('}') + 1]
            self.jsonres = json.loads(jsons)
            print(self.jsonres)
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True

        except Exception as e:
            # 异常处理的时候，分析逻辑问题
            self.jsonres = {}
            logger.exception(e)

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    def removeheader(self, key):

        try:
            self.session.headers.pop(key)
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        except Exception as e:
            logger.error('没有' + key + '这个键的header存在')
            logger.exception(e)
            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    def addheader(self, key, value):
        try:
            value = self.__get_param(value)
            self.session.headers[key] = value
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        except Exception as e:
            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    # def assertequals(self, key, value):
    def assertequals(self, jpath, value):

        value = self.__get_param(value)
        res = str(self.result)
        try:
            res = str(jsonpath.jsonpath(self.jsonres, jpath)[0])
            print(res)
        except Exception as e:
            pass
        if res == str(value):

            logger.info('PASS')
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        else:
            logger.info('FAIL')
            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    def assertin(self, jpath, value):
        """
        断言是否包含，不建议用这个
        :param jpath:
        :param value:
        :return:
        """

        value = self.__get_param(value)
        res = str(self.result)
        try:
            res = str(jsonpath.jsonpath(self.jsonres, jpath)[0])

        except Exception as e:
            pass
        if res in str(value):

            logger.info('PASS')
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        else:
            logger.info('FAIL')
            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    def savejson(self, jpath, p):

        try:
            self.params[p] = str(jsonpath.jsonpath(self.jsonres, jpath)[0])
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            # 调试使用
            print(self.params[p])
            return True

        except Exception as e:

            logger.error("error：保存参数失败！没有" + jpath + "这个键。")

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False

    def __get_param(self, s):

        for key in self.params:
            s = s.replace('{' + key + '}', str(self.params[key]))
            # s = s.replace('{' + key + '}', self.params[key])
            print(s)

        return s

    def __get_data(self, s):

        flg = False

        param = {}
        p = s.split('&')

        for pp in p:

            ppp = pp.split('=')

            try:
                param[ppp[0]] = ppp[1]
            except Exception as e:

                flg = True

                logger.error('error：URL参数为JSON格式！')

                logger.exception(e)

        if flg:
            s = s.encode('utf-8')

            return s
        else:
            return param

    def gettime(self, nowdata, da):

        now = datetime.datetime.now()
        if da == 0:
            self.params[nowdata] = now.strftime('%Y-%m-%d')
            print(self.params[nowdata])
        else:
            delta = datetime.timedelta(days=da)
            n_days = now + delta
            self.params[nowdata] = n_days.strftime('%Y-%m-%d')
            print(self.params[nowdata])
        self.writer.write(self.writer.row + 1, 8, 'PASS')
        return True

    def getvalcode(self, mobile, numb):

        conn = pymysql.connect(host='192.168.1.246', port=3306, user='ydh_test', password='ydh_test_123',
                               database='ydh_test', charset='utf8')
        cur = conn.cursor()

        SQL = "SELECT verification_code FROM validation_code WHERE account =%s;"
        try:
            cur.execute(SQL, mobile)
            conn.commit()
            # 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.params[numb] = row[0]
                # print("code=%s" % (code))
                print(self.params[numb])
                self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        except Exception as e:

            logger.error("error：获取验证码失败！")

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False
        # 关闭游标和连接
        cur.close()
        conn.close()

    def getrequestId(self, phone, tid):
        conn = pymysql.connect(host='192.168.1.246', port=3306, user='ydh_test', password='ydh_test_123',
                               database='ydh_test', charset='utf8')
        cur = conn.cursor()

        SQL1 = "SELECT id FROM ydh_buyer_request WHERE contact_phone =%s;"
        try:
            cur.execute(SQL1, phone)
            conn.commit()
            # 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.params[tid] = row[0]
                print(self.params[tid])
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        except Exception as e:

            logger.error("error：获取requestId失败！")

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False
        # 关闭游标和连接
        cur.close()
        conn.close()

    # def getbuyerId(self, phone, bid):
    #     conn = pymysql.connect(host='192.168.1.246', port=3306, user='ydh_test', password='ydh_test_123',
    #                            database='ydh_test', charset='utf8')
    #     cur = conn.cursor()
    #
    #     SQL2 = "SELECT buyer_id FROM ydh_buyer_request WHERE contact_phone =%s AND status='processing' AND seller_id='2';"
    #     print(SQL2)
    #     try:
    #         cur.execute(SQL2, phone)
    #         conn.commit()
    #         # 获取所有记录列表
    #         results = cur.fetchall()
    #
    #         for row in results:
    #             self.params[bid] = row[0]
    #             print(self.params[bid])
    #         self.writer.write(self.writer.row + 1, 8, 'PASS')
    #         return True
    #     except Exception as e:
    #
    #         logger.error("error：获取buyerId失败！")
    #
    #         self.writer.write(self.writer.row + 1, 8, 'FAIL')
    #         return False
    #     # 关闭游标和连接
    #     cur.close()
    #     conn.close()

    def getbuyerId(self, phone, sid, bid):
        conn = pymysql.connect(host='192.168.1.246', port=3306, user='ydh_test', password='ydh_test_123',
                               database='ydh_test', charset='utf8')
        cur = conn.cursor()

        SQL2 = "SELECT buyer_id FROM ydh_buyer_request WHERE contact_phone =%(tel)s AND status='processing' AND seller_id=%(id)s;"
        print(SQL2)
        value = {
            "tel": phone,
            "id": sid
        }
        try:
            cur.execute(SQL2, value)
            conn.commit()
            # 获取所有记录列表
            results = cur.fetchall()

            for row in results:
                self.params[bid] = row[0]
                print(self.params[bid])
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        except Exception as e:

            logger.error("error：获取buyerId失败！")

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False
        # 关闭游标和连接
        cur.close()
        conn.close()

    def getrequestIdd(self, phone, tid):
        conn = pymysql.connect(host='192.168.1.246', port=3306, user='ydh_test', password='ydh_test_123',
                               database='ydh_test', charset='utf8')
        cur = conn.cursor()

        SQL1 = "SELECT id FROM ydh_buyer_request WHERE contact_phone =%s AND status='processing' AND seller_id='2';"
        try:
            cur.execute(SQL1, phone)
            conn.commit()
            # 获取所有记录列表
            results = cur.fetchall()
            for row in results:
                self.params[tid] = row[0]
                print(self.params[tid])
            self.writer.write(self.writer.row + 1, 8, 'PASS')
            return True
        except Exception as e:

            logger.error("error：获取requestId失败！")

            self.writer.write(self.writer.row + 1, 8, 'FAIL')
            return False
        # 关闭游标和连接
        cur.close()
        conn.close()
