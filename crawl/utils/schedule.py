# -*- coding: UTF-8 -*-
"""
@Author ：haby0
@Desc   ：
"""
import schedule
import time
import datetime
from utils.logger import LoggerUtil
from utils.engine import Engine
from utils.mail import MailUtil

logger = LoggerUtil().get_log

class Schedule(object):
    def __init__(self):
        pass

    def blogJob(self):
        logger.info('blogJob-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        engine = Engine()
        urls = engine.get_url()
        logger.info('urls : ' + str(len(urls.keys())))
        deduplicationUrls = engine.deduplication()
        logger.info('deduplicationUrls : ' + str(len(urls.keys())))
        if len(deduplicationUrls) > 0:
            engine.download_file()
            # engine.senMail()
        logger.info('blogJob-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def blogJobDay(self):
        logger.info('blogJob-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        messages = Engine().getYesterdayUrls()
        MailUtil().senHtml(messages)
        logger.info('blogJob-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    def start(self):
        # self.blogJob()
        # self.blogJobDay()
        schedule.every(5).minutes.do(self.blogJob)
        schedule.every().day.at('8:00').do(self.blogJobDay)
        while True:
            schedule.run_pending()
