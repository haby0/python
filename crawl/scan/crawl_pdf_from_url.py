# -*- coding: UTF-8 -*-
"""
@Author ：haby0
@Desc   ：
"""
import importlib,sys
importlib.reload(sys)
import ssl
import pdfkit
from utils.config import *

ssl._create_default_https_context = ssl._create_unverified_context

logger = LoggerUtil().get_log

def make_pdf_from_url(url, src, title):
    try:
        filename = "{title}.pdf".format(title=title)

        logger.info("makeing {filename} from {url} ...".format(filename=filename, url=url))

        path_wk = project_path + '/wkhtmltox/bin/wkhtmltopdf.exe'  # 安装位置

        config = pdfkit.configuration(wkhtmltopdf = path_wk)

        options = {
            'page-size': 'Letter',
            'encoding': "UTF-8",
            'custom-header': [
                ('Connection', 'close'),
                ('Upgrade-Insecure-Requests', '1'),
                ('Sec-Fetch-User', '?1'),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
                ('Sec-Fetch-Site', 'same-origin'),
                ('Sec-Fetch-Mode', 'navigate'),
                ('Accept - Encoding', 'gzip, deflate'),
                ('Accept-Language', 'zh-CN,zh;q=0.9'),
                ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')
            ],
        }

        filepath = project_path + '/pdf/' + src + '/' + title.replace('\u200b', '').strip() + '.pdf'

        logger.info("download file path : {filepath}".format(filepath=filepath))

        result = pdfkit.from_url(url, filepath, options=options, configuration=config)
    except Exception as e:
        logger.error(str(e))
        result = False

    return result

# print(make_pdf_from_url( 'https://www.anquanke.com/post/id/200312', 'anquanke', '恶意流量分析实践系列一'))