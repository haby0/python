# -*- coding: UTF-8 -*-
"""
@Author ：haby0
@Desc   ：
"""

import threading

class ThreadHandler(threading.Thread):
    def __init__(self, num):
        # 执行父类的构造方法
        threading.Thread.__init__(self)
        # 传入参数 num
        self.num = num

    # 定义每个线程要运行的函数
    def run(self):
        while self.num > 0:
            print("当前线程数:", threading.activeCount())
            self.num -= 1