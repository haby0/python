# -*- coding: UTF-8 -*-
"""
@Author ：haby0
@Desc   ：
"""
from mitmproxy import ctx
from mitmproxy import http


class Counter:
    def __init__(self):
        pass

    def request(self, flow):
        url = "https://" + flow.request.headers["Host"] + flow.request.path
        ctx.log.info(url)
        proxy = ("localhost", 8088)
        if flow.live:
            flow.live.change_upstream_proxy_server(proxy)

    def response(self, flow):
        ctx.log.info(flow.response.headers['Content-Type'])


addons = [
    Counter()
]

