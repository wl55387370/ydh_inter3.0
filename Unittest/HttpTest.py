# -*- coding:utf-8 -*-
# @Time    :2019/8/29 0029 11:17
# @Author  :wulin
# @Mail    :286075568@qq.com
# @FileName: HttpTest.py
# @Software: PyCharm

import unittest, datetime, time
from parameterized import parameterized
from common.http_request import HTTP
from Unittest import datadriven


class TestHttp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.obj = None

        if datadriven.runtype == 'HTTP':
            cls.obj = HTTP(datadriven.writer)


    @parameterized.expand(datadriven.alllist)
    def test_all(self, index, name, key, param1, param2, param3):
        """"""
        print(name)

        flg = False
        try:
            index = int(index)


            datadriven.writer.row = index

            flg = True
        except:

            datadriven.writer.set_sheet(index)

        if flg:
            line = [key, param1, param2, param3]
            print(line)

            func = datadriven.geffunc(line, self.obj)

            lenargs = datadriven.getargs(func)

            res = datadriven.run(func, lenargs, line)

            if res == False:
                self.fail('关键字执行失败')
