# -*- coding: utf-8 -*-
# @Time    : 2019/12/3 0003 11:11
# @Author  : wulin
# @Email   :286075568@qq.com
# @FileName: email.py
# @Software: PyCharm


import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common.outlog import MyLog

logger = MyLog('INFO')


class EmailSend:

    def __init__(self):
        self.sender = 'm18570394312_1@163.com'
        self.receiver = '286075568@qq.com'
        self.smtpserver = 'smtp.163.com'
        self.username = 'm18570394312_1@163.com'
        self.password = 'dongnao001'
        self.mail_title = '主题：这是测试邮件'

    def send_email(self):
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = self.sender
        message['To'] = self.receiver
        message['Subject'] = Header(self.mail_title, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText('这是邮件的正文', 'plain', 'utf-8'))
        #
        # # 构造附件1（附件为TXT格式的文本）
        # att1 = MIMEText(open('text1.txt', 'rb').read(), 'base64', 'utf-8')
        # att1["Content-Type"] = 'application/octet-stream'
        # att1["Content-Disposition"] = 'attachment; filename="text1.txt"'
        # message.attach(att1)

        # # 构造附件2（附件为JPG格式的图片）
        # att2 = MIMEText(open('123.jpg', 'rb').read(), 'base64', 'utf-8')
        # att2["Content-Type"] = 'application/octet-stream'
        # att2["Content-Disposition"] = 'attachment; filename="123.jpg"'
        # message.attach(att2)

        # 构造附件3（附件为HTML格式的网页）
        att3 = MIMEText(open('D:\\github\\ydh_testinter3.0\\test_result\\html_report', 'rb').read(), 'base64', 'utf-8')
        att3["Content-Type"] = 'application/octet-stream'
        att3["Content-Disposition"] = 'attachment; filename="report_test.html"'
        message.attach(att3)

        smtpObj = smtplib.SMTP_SSL()  # 注意：如果遇到发送失败的情况（提示远程主机拒接连接），这里要使用SMTP_SSL方法
        smtpObj.connect(self.smtpserver)
        smtpObj.login(self.username, self.password)
        smtpObj.sendmail(self.sender, self.receiver, message.as_string())
        print("邮件发送成功！！！")
        smtpObj.quit()

# class Mail:
#     """
#         用来发送邮件
#     """
#
#     def __init__(self):
#         self.mail_info = {}
#         # 发件人
#         self.mail_info['from'] = 'm18570394312_1@163.com'
#         self.mail_info['username'] = 'm18570394312_1@163.com'
#         # smtp服务器域名
#         self.mail_info['hostname'] = 'smtp.163.com'
#         # 发件人的密码
#         self.mail_info['password'] = 'dongnao001'
#         # 收件人
#         self.mail_info['to'] = '286075568@qq.com'
#         # 抄送人
#         self.mail_info['cc'] = '1416084196@qq.com'
#         # 邮件标题
#         self.mail_info['mail_subject'] = '自动化测试报告'
#         self.mail_info['mail_encoding'] = 'utf8'
#         # 附件内容
#         self.mail_info['filepaths'] = []
#         self.mail_info['filenames'] = []
#
#     def send(self, text):
#         # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587
#         smtp = SMTP_SSL(self.mail_info['hostname'])
#         smtp.set_debuglevel(0)
#
#         ''' SMTP 'ehlo' command.
#         Hostname to send for this command defaults to the FQDN of the local
#         host.
#         '''
#         smtp.ehlo(self.mail_info['hostname'])
#         smtp.login(self.mail_info['username'], self.mail_info['password'])
#
#         # 普通HTML邮件
#         # msg = MIMEText(text, 'html', self.mail_info['mail_encoding'])
#
#         # 支持附件的邮件
#         msg = MIMEMultipart()
#         msg.attach(MIMEText(text, 'html', self.mail_info['mail_encoding']))
#
#         msg['Subject'] = Header(self.mail_info['mail_subject'], self.mail_info['mail_encoding'])
#         # 设置发件人昵称
#         msg['from'] = self.mail_info['from']
#         # msg['from'] = 'Antoy'
#
#         logger.debug(self.mail_info)
#         logger.debug(text)
#         msg['to'] = ','.join(self.mail_info['to'])
#         receive = self.mail_info['to']
#         # 处理抄送列表为空的情况
#         if self.mail_info['cc'] is None or self.mail_info['cc'][0] == '':
#             # 没有添加抄送列表的时候，不抄送
#             pass
#         else:
#             msg['cc'] = ','.join(self.mail_info['cc'])
#             receive += self.mail_info['cc']
#
#         # 添加附件
#         for i in range(len(self.mail_info['filepaths'])):
#             att1 = MIMEText(open(self.mail_info['filepaths'][i], 'rb').read(), 'base64', 'utf-8')
#             att1['Content-Type'] = 'application/octet-stream'
#             att1['Content-Disposition'] = 'attachment; filename= "' + self.mail_info['filenames'][i] + '"'
#             msg.attach(att1)
#
#         try:
#             smtp.sendmail(self.mail_info['from'], receive, msg.as_string())
#             smtp.quit()
#             logger.info('邮件发送成功')
#         except Exception as e:
#             logger.error('邮件发送失败：')
#             logger.exception(e)
#
#
# if __name__ == '__main__':
#
#     mail = Mail()
#     mail.send('测试')
#     mail.mail_info['filepaths'] = ['./test_result/html_report/ydh_inter.html']
#     mail.mail_info['filenames'] = ['ydh_inter.html']


