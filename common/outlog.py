# -*- coding:utf-8 -*-
# @Time    :2019/11/8 0008 13:03
# @Author  :wulin
# @Mail    :286075568@qq.com
# @FileName: logging.py
# @Software: PyCharm

import logging, time


# 日志收集器

class MyLog:
    def __init__(self, log_name):
        self.log_name = log_name  # 日志收集器的名字

    def my_log(self, msg, level):
        logger = logging.getLogger(self.log_name)
        logger.setLevel('DEBUG')  # 包含INFO级别在内以及以上的日志
        # 格式：决定我们日志输出格式
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息：%(message)s')
        # 2日志输出器 控制台、指定的文件
        ch = logging.StreamHandler()  # 渠道是指输出到控制台
        ch.setLevel('DEBUG')  # 只输出INFO以上的
        ch.setFormatter(formatter)

        now = time.strftime('%Y-%m-%d')  # 获取到当天的时间
        path = "./test_result/log_txt/ydh_api_" + now + ".txt"  # 拼接路径
        # 最终日志存放的地方
        fh = logging.FileHandler(path, encoding='UTF-8')
        fh.setLevel('DEBUG')
        fh.setFormatter(formatter)
        # 3 对接
        logger.addHandler(ch)
        logger.addHandler(fh)

        if level == 'DEBUG':
            logger.debug(msg)
        elif level == 'INFO':
            logger.info(msg)
        elif level == 'WARNING':
            logger.warning(msg)
        elif level == 'ERROR':
            logger.error(msg)
        elif level == 'CRITICAL':
            logger.critical(msg)

        logger.removeHandler(ch)
        logger.removeHandler(fh)

    def debug(self, msg):
        self.my_log(msg, 'DEBUG')

    def info(self, msg):
        self.my_log(msg, 'INFO')

    def warning(self, msg):
        self.my_log(msg, 'WARNING')

    def error(self, msg):
        self.my_log(msg, 'ERROR')

    def critical(self, msg):
        self.my_log(msg, 'CRITICAL')
