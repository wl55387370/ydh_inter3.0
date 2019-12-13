# -*- coding: utf-8 -*-
# @Time    : 2019/11/18 0018 11:15
# @Author  : wulin
# @Email   :286075568@qq.com
# @FileName: mysql.py
# @Software: PyCharm

# 导入pymysql模块
import pymysql
from common.outlog import MyLog



# 导入pymysql模块
import pymysql
from common.outlog import MyLog
logger=MyLog('INFO')


# 连接database
class Mysql:
    def __init__(self):
        # 配置mysql参数
        self.mysql_info= {
            'mysqluser': "ydh_test",
            'mysqlpassword': "ydh_test_123",
            'mysqlport': 3306,
            'mysqlhost': '192.168.1.246',
            'mysqldb': 'ydh_test',
            'mysqlcharset': "utf8"
        }

        # 初始化mysql配置

    def init_mysql(self):

        # 创建连接，执行语句的时候是在这个连接
        connect = pymysql.connect(
            user=self.mysql_info['mysqluser'],
            password=self.mysql_info['mysqlpassword'],
            port=self.mysql_info['mysqlport'],
            host=self.mysql_info['mysqlhost'],
            db=self.mysql_info['mysqldb'],
            charset=self.mysql_info['mysqlcharset']
        )

        self.cursor = connect.cursor()


    def execute_mysql(self):
        # 获取游标


        logger.info("正在恢复%ydh_test%数据库商户数据")
        # 一行一行执行SQL语句
        # 后台一级创建商户
        sql = "DELETE FROM ydh_buyer WHERE mobile='19900000001';"
        sql1 = "DELETE FROM ydh_buyer_account WHERE account_key='19900000001';"
        sql2 = "DELETE FROM ydh_buyer_address WHERE tel='19900000001';"
        # 后台二级创建商户

        sql3 = "DELETE FROM ydh_buyer WHERE mobile='19900000002';"
        sql4 = "DELETE FROM ydh_buyer_account WHERE account_key='19900000002';"
        sql5 = "DELETE FROM ydh_buyer_address WHERE tel='19900000002';"
        # 开放注册
        sql6="DELETE FROM ypm_buyer_request WHERE buyer_id=(SELECT id FROM ydh_buyer WHERE mobile='13400000145' );"
        sql7 = "DELETE FROM ydh_buyer WHERE mobile='13400000145';"
        sql8 = "DELETE FROM ydh_buyer_account WHERE account_key='13400000145';"
        sql9="DELETE FROM ydh_buyer_request WHERE contact_phone='13400000145';"
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            logger.info("一级商家数据删除成功！")

            self.cursor.execute(sql3)
            self.cursor.execute(sql4)
            self.cursor.execute(sql5)
            logger.info("二级商家数据删除成功！")
            self.cursor.execute(sql6)
            self.cursor.execute(sql7)
            self.cursor.execute(sql8)
            self.cursor.execute(sql9)
            logger.info("开放注册商家数据删除成功！")
            self.init_mysql().commit()


        except:
            print
            "Error: unable to fecth data"

            # 关闭游标和连接
            self.cursor.close()
            self.init_mysql().close()

    # def select_mysql(self):
    #     # 获取游标
    #     cursor = self.init_mysql().cursor()
    #
    #     logger.info("正在查询%ydh_test%数据库商户数据")
    #     se1 = "SELECT id FROM ydh_buyer_request WHERE contact_phone =%s;"
    #     cursor.execute(se1)
    #     self.init_mysql().commit()
    #     # 关闭游标和连接
    #     cursor.close()
    #     self.init_mysql().close()


# 调试代码
if __name__ == '__main__':

    mysql = Mysql()
    mysql.init_mysql()


