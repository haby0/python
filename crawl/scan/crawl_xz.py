# -*- coding: utf-8 -*-
import sys
import urllib.request
import ssl
from utils.logger import LoggerUtil
from lxml import etree

ssl._create_default_https_context = ssl._create_unverified_context

class CrawlXz():
    def __init__(self, url):
        self.logger = LoggerUtil().get_log
        # 请求 url
        self.url = url
        # 构建代理 handler
        # self.proxy_list = {
        #     "http" : "127.0.0.1:8080",
        #     "https": "127.0.0.1:8080"
        # }
        self.proxy_list = None

    def do_request(self):
        try:
            # 创建代理处理器
            httpproxy_handler = urllib.request.ProxyHandler(self.proxy_list)
            # 创建特定的opener对象
            opener = urllib.request.build_opener(httpproxy_handler, urllib.request.HTTPSHandler)
            # 安装全局的opener 把urlopen也变成特定的opener
            urllib.request.install_opener(opener)

            # http头信息
            headers = {
                'Connection': 'close',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-User': '?1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Accept - Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            }
            req = urllib.request.Request(self.url, headers = headers)

            return urllib.request.urlopen(req, timeout=60).read().decode("utf8")  # timeout_sec指定超时时间

        except Exception as e:
            self.logger.error(sys._getframe().f_code.co_name + " error : " + str(e))

    def parse(self):
        res = self.do_request()
        # 构建 html 树
        html = etree.HTML(res)
        # xpath 解析 html
        items = html.xpath('//*[@class="topic-title"]')

        urls = {}
        # 获取 urls
        for item in items:
            urls['https://xz.aliyun.com' + item.attrib['href']] = item.text.replace('\u200b', '').strip()
        return urls
