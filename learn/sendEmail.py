#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.header import Header
from email.mime.text import MIMEText

# 设置邮件头部显示
message = MIMEText("邮件测试", 'plain', 'utf-8')  # 邮件发送正文(随意定义)
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')  # 邮件显示主题(随意定义)
message['From'] = '孔扎根'  # 邮件显示发件人(随意定义)
message['To'] = '天心明月'  # 邮件显示收件人(随意定义)

#附件（可选）
attr = MIMEText(open('./201812.csv', 'rb').read(),'base64', 'utf-8')  # 封装邮件内容
attr['Content-Type'] = 'application/octet-stream'
attr['Content-Disposition'] = 'attachment; filename =' + '201812.csv'
message.attach(attr)  # 添加到实例(文件形式)

# 配置服务器及账号信息
sender = 'xx@xxx.cn'  # 发件人
receivers = ['xxxx@qq.com']  # 收件人
mail_host = 'smtp.xxxx.cn'  # 发送邮件smtp服务器
mail_user = 'xxxx@xxxx.cn'  # 登陆邮箱账号
mail_pass = 'xxxxxzzz!'  # 登陆邮箱密码

try:
    smtpObj = smtplib.SMTP()  # 构造smtp实例
    smtpObj.connect(mail_host, 25)  # 连接smtp服务器
    smtpObj.login(mail_user, mail_pass)  # 登陆邮箱
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送邮件正文
    print("OK")
except:
    print("err")
