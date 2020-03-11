import logging
import os

class LoggerUtil(object):
    def __init__(self, name=__name__):
        # 创建一个loggger
        self.__name = name
        self.logger = logging.getLogger(self.__name)

        # 清理 handler
        self.logger.handlers.clear()

        # 设置日志最低输出级别
        self.logger.setLevel(logging.DEBUG)

        log_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), "log\crawl.log")

        # fh = logging.handlers.TimedRotatingFileHandler(logname, when='M', interval=1, backupCount=5,encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        # 不拆分日志文件，a指追加模式,w为覆盖模式
        logger =  logging.getLogger()


        fh = logging.FileHandler(log_path, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # 创建一个handler，用于将日志输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(filename)s-[line:%(lineno)d]'
                                      '-%(levelname)s : %(message)s',
                                      datefmt='%a, %d %b %Y %H:%M:%S')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def get_log(self):
        """定义一个函数，回调logger实例"""
        return self.logger