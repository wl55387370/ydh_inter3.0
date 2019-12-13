# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 0026 9:18
# @Author  : wulin
# @Email   :286075568@qq.com
# @FileName: runhtml.py
# @Software: PyCharm


import unittest, sys
from BeautifulReport import BeautifulReport as bf
from Unittest import datadriven

from common.outlog import MyLog
from common.mysql import Mysql

# 运行的相对路径
path = '.'
# 用例路径
casepath = ''
resultpath = ''
logger = MyLog('INFO')

if __name__ == '__main__':

    mysql = Mysql()
    mysql.init_mysql()


    try:
        casepath = sys.argv[1]
    except:
        casepath = ''

    # 为空，则使用默认的
    if casepath == '':
        casepath = path + '/excel_case/http_ydh.xlsx'
        # resultpath = ''
        resultpath = path + '/test_result/excel_result/result_http_ydh.xlsx'
    else:
        # 如果是绝对路径，就使用绝对路径
        if casepath.find(':') >= 0:
            # 获取用例文件名
            resultpath = path + '/test_result/excel_result/result-' + casepath[casepath.rfind('\\') + 1:]

        else:
            logger.error('用例路径不存在!')

    datadriven.getparams(casepath, resultpath)

    suite = unittest.defaultTestLoader.discover("./Unittest/", pattern="HttpTest.py", top_level_dir=None)
    # 生成执行用例的对象
    runner = bf(suite)
    runner.report(filename='./test_result/html_report/ydh_inter.html', description=datadriven.title)
    datadriven.writer.save_close()
