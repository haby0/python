# -*- coding: UTF-8 -*-
"""
@Author ：haby0
@Desc   ：
"""
from scan.crawl_xz import CrawlXz
from scan.crawl_anquanke import CrawlAqk
from utils.mysql import *
from scan.crawl_pdf_from_url import *
from utils.mail import MailUtil
from utils.config import *
import time
import hashlib

class Engine(object):
    def __init__(self):
        self.urls = {}
        self.yeUrls = {}
        pass

    def get_url(self):
        xzUrls = CrawlXz("https://xz.aliyun.com/?page=1").parse()
        aqkUrls = CrawlAqk("https://www.anquanke.com/knowledge").parse()
        if len(xzUrls) != 0:
            self.urls.update(xzUrls)
        if len(aqkUrls) != 0:
            self.urls.update(aqkUrls)
        return self.urls


    def deduplication(self):
        if len(self.urls) == 0:
            logger.info('urls is null')
        else:
            # python 字典遍历时不能做删除，改为 list
            for url in list(self.urls):
                if 'xz' in url:
                    src = 'xz'
                elif 'anquanke' in url:
                    src = 'anquanke'
                md5hash = hashlib.md5(url.encode('utf-8')).hexdigest()
                title = self.urls[url]
                logger.info('url info : {src}  {url}  {md5hash}  {title}'.format(src=src, url=url, md5hash=md5hash, title=title))

                result = MySqlHandle().selectDB('select * from blogurl where md5hash = "' + md5hash + '"')
                logger.info('selct result : ' + str( result))
                if len(result) > 0:
                    if result[0][5] == '1':
                        self.urls.pop(url)
                        logger.info('url: {url} already exists and downloaded'.format(url=url))
                    logger.info('url: {url} already exists but not downloaded'.format(url=url))
                else:
                    status = 0
                    insertResult = MySqlHandle().insertDB('insert into blogurl(src, url, title, md5hash, status, inserttime) values '
                                                          '("' + src + '","' + url + '","' + title + '","' + md5hash + '","' + str(status) +'","' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '")')
                    logger.info('insertResult : ' + str(insertResult))
                    if insertResult == 0:
                        MailUtil().sendError('插入数据库异常 : ' + src + '  ' + title + '  ' + url)
        return self.urls

    def download_file(self):
        for url in list(self.urls):
            if 'xz' in url:
                src = 'xz'
            elif 'anquanke' in url:
                src = 'anquanke'
            filepath = project_path + '/pdf/' + src + '/' + self.urls[url].replace('\u200b', '').strip() + '.pdf'
            if not os.path.exists(filepath):
                if (make_pdf_from_url(url, src, self.urls[url]) == False):
                    # html 转换 pdf 异常就不发送邮件了，从 url 中删除
                    self.urls.pop(url)
                    MailUtil().sendError(src + ' 文章转换 pdf 异常: ' + url)
            else:
                logger.info('file already exists : ' + url)

        return True

    def senMail(self):
        for url in self.urls:
            if 'xz' in url:
                src = 'xz'
            elif 'anquanke' in url:
                src = 'anquanke'
            md5hash = hashlib.md5(url.encode('utf-8')).hexdigest()
            result = MySqlHandle().selectDB('select * from blogurl where md5hash = "' + md5hash + '"')
            if len(result) > 0:
                if result[0][5] == '0':
                    if MailUtil().sendPdf(src, self.urls[url], url, (project_path + '/pdf/' + src + '/' + self.urls[url].replace('\u200b', '').strip() + '.pdf')) == True:
                        MySqlHandle().updateDB('update blogurl set status = "1"  where md5hash = "' + md5hash + '"')
                        logger.info('Send pdf email successfully : ' + src + '    ' + self.urls[url] + '.pdf')
                    else:
                        logger.info('Send pdf email failed : ' + src + '    ' + self.urls[url] + '.pdf')

    def getYesterdayUrls(self):
        result = MySqlHandle().selectDB('select * from blogurl where date(inserttime) = date_sub(curdate(),interval 1 day)')
        # result = MySqlHandle().selectDB('select * from blogurl where date(inserttime) = curdate()')
        messages = {}
        for url in result:
            messages.setdefault(url[1], {})[url[2]]=url[3]
        return messages