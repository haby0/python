# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from smtplib import SMTPException
from utils.config import *
from utils.logger import LoggerUtil
import random
import traceback

logger = LoggerUtil().get_log

class MailUtil(object):
    def __init__(self):
        self.host = ConfigParser().get_config('mail2', 'host')
        self.port = ConfigParser().get_config('mail2', 'port')
        self.mails = ConfigParser().get_config('mail2', 'mails')
        self.fromaddr = ConfigParser().get_config('mail2', 'from')
        self.password = ConfigParser().get_config('mail2', 'password')
        self.toaddr = ConfigParser().get_config('mail2', 'to')
        self.ccaddr = ConfigParser().get_config('mail2', 'cc')

        logger.info('email property data : host:{host} -- port:{port} -- mails:{mails} -- fromaddr:{fromaddr} -- toaddr:{toaddr} -- ccaddr:{ccaddr}'.format(
            host=self.host,
            port=self.port,
            mails=self.mails,
            fromaddr=self.fromaddr,
            toaddr=self.toaddr,
            ccaddr=self.ccaddr
        ))

    def sendError(self, e):
        msg = MIMEMultipart()
        mails = self.mails.split(',')  # 可以写多个邮箱
        mail = random.choice(mails)  # 随机选择一个
        msg['Subject'] = '邮件发送异常'
        msg['From'] = '{0} <{1}>'.format(mail, self.fromaddr)
        # 支持多用户接收邮件
        msg['To'] = self.toaddr
        msg['Cc'] = self.ccaddr

        # 下面是文字部分，也就是纯文本
        puretext = MIMEText('异常内容：' + e)
        msg.attach(puretext)
        self.sendMail(msg)

    def sendMail(self, msg):
        mails = self.mails.split(',')  # 可以写多个邮箱
        mail = random.choice(mails)  # 随机选择一个
        host = self.host.strip()
        port = self.port.strip()

        try:
            if port == '465':
                port = int(port)
                s = smtplib.SMTP_SSL(host, port)
            else:
                s = smtplib.SMTP(host, port)
                s.ehlo()
                s.starttls()
            s.ehlo()
            s.login(mail, self.password)
            s.sendmail(mail, self.toaddr.split(',') + self.ccaddr.split(','), msg.as_string())
            s.quit()
            logger.info('Send mail Success')
            return True
        except SMTPException as e:
            logger.error('Send mail failed')
            self.sendError(str(e))
            traceback.print_exc()
            return False

    def senHtml(self, messages):
        htmlHead = open(config_dir + '/htmlHead', 'r').read()
        htmlTail = open(config_dir + '/htmlTail', 'r').read()

        htmlText = ''

        for key in messages:
            if key == 'xz':
                src = '先知'
            elif key == 'anquanke':
                src = '安全客'
            htmlText = htmlText + '<tr><td align="left" style="font-size: 17px; color:#595757; line-height:25px;"><b>' \
                   + src + \
                   '</b></td></tr>'
            for url in messages[key]:
                htmlText = htmlText + ('<tr><td align="left" valign="top" style="font-size:15px; color:#595757; font-size:14px; line-height: 25px; font-family:Hiragino Sans GB; padding: 15px 0 0 0"><a href="' \
                       + url +\
                       '">'\
                       + messages[key][url] + '</a><a></a></td></tr><tr>')

        html = htmlHead + htmlText + htmlTail

        msg = MIMEMultipart()
        mails = self.mails.split(',')  # 可以写多个邮箱
        mail = random.choice(mails)  # 随机选择一个
        msg['Subject'] = '安全晨报'
        msg['From'] = '{0} <{1}>'.format(mail, self.fromaddr)
        # 支持多用户接收邮件
        msg['To'] = self.toaddr
        msg['Cc'] = self.ccaddr

        # 下面是文字部分，也就是纯文本
        msg.attach(MIMEText(html, _subtype='html', _charset='utf-8'))

        return self.sendMail(msg)

    def sendPdf(self, src, title, url, filepath):
        logger.info('sendpdf message : {src}  {title}  {url}  {filepath}'.format(src=src, title=title, url=url, filepath=filepath) )
        msg = MIMEMultipart()
        mails = self.mails.split(',')  # 可以写多个邮箱
        mail = random.choice(mails)  # 随机选择一个
        if src == 'xz':
            msg['Subject'] = '先知'
        elif src == 'anquanke':
            msg['Subject'] = '安全客'
        msg['From'] = '{0} <{1}>'.format(mail, self.fromaddr)
        # 支持多用户接收邮件
        msg['To'] = self.toaddr
        msg['Cc'] = self.ccaddr

        # 下面是文字部分，也就是纯文本
        puretext = MIMEText(url)
        msg.attach(puretext)

        pdfPart = MIMEApplication(open(filepath, 'rb').read())
        pdfPart.add_header('Content-Disposition', 'attachment', filename = title + '.pdf')
        msg.attach(pdfPart)
        return self.sendMail(msg)

    def setContext(self, src, url, context, contextType):
        self.src = src
        self.url = url
        self.context = context
        self.contextType = contextType