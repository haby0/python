# -*- coding: utf-8 -*-
import importlib,sys
from utils.logger import LoggerUtil
importlib.reload(sys) # 重新加载 sys 模块

import urllib
import urllib.request

from lxml import etree
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class CrawlAqk():
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
        items = html.xpath('//*[@class="article-item common-item"]/div/div[2]/div/div[1]')

        urls = {}
        # 获取 urls
        for item in items:
            link = item.xpath('a')[0]
            urls['https://www.anquanke.com' + link.attrib['href']] = link.text.replace('\u200b', '').strip()
        return urls
