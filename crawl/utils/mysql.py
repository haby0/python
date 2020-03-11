# -*- coding: UTF-8 -*-
"""
@Author ：haby0
@Desc   ：
"""
import pymysql
from utils.config import ConfigParser
from utils.logger import LoggerUtil
from utils.mail import MailUtil

logger = LoggerUtil().get_log

class MySqlHandle(object):
    def __init__(self):
        self.host = ConfigParser.get_config('MySQL', 'host')
        self.port = ConfigParser.get_config('MySQL', 'port')
        self.username = ConfigParser.get_config('MySQL', 'username')
        self.password = ConfigParser.get_config('MySQL', 'password')
        self.dbname = ConfigParser.get_config('MySQL', 'dbname')
        try:
            # 连接数据库
            connect = pymysql.Connect(
                host = self.host,
                port = int(self.port),
                user = self.username,
                passwd = self.password,
                db = self.dbname,
                charset = 'utf8'
            )
        except Exception as e:
            logger.error('database conn error : {e}'.format(e=e))

        self.conn = connect

        logger.info("host : {host} -- port : {port} -- username : {username} -- password : {password} -- database : {database}".format(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.dbname,
        ))

    def updateDB(self, sql):
        logger.info("sql : {sql}".format(sql=sql))
        '''更新数据库操作'''
        self.cursor = self.conn.cursor()
        try:
            result = self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 回滚
            self.conn.rollback()
            logger.error("update data error : {e}".format(e=e))
            MailUtil().sendError('更新数据库异常 : ' + e)
        finally:
            self.cursor.close()
            self.conn.close()

    def insertDB(self, sql):
        '''插入数据库操作'''
        logger.info("sql : {sql}".format(sql=sql))

        self.cursor = self.conn.cursor()
        result = 0
        try:
            result = self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 回滚
            self.conn.rollback()
            result = 0
            logger.error("insert data error : {e}".format(e=e))
            MailUtil().sendError('插入数据库异常 : ' + e)
        finally:
            self.cursor.close()
            self.conn.close()
        return result

    def selectDB(self, sql):
        ''' 数据库查询 '''
        logger.info("sql : {sql}".format(sql=sql))

        self.cursor = self.conn.cursor()
        result = 0
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e:
            logger.error("select data error : {e}".format(e=e))
            MailUtil().sendError('查询数据库异常 : ' + e)
        finally:
            self.cursor.close()
            self.conn.close()
        return result

    def deleteDB(self, sql):
        ''' 操作数据库数据删除 '''
        logger.info("sql : {sql}".format(sql=sql))

        self.cursor = self.conn.cursor()

        try:
            # 执行sql
            result = self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            # 发生错误时回滚
            self.conn.rollback()
            logger.error("insert data error : {e}".format(e=e))
            MailUtil().sendError('删除数据库异常 : ' + e)
        finally:
            self.cursor.close()

    def closeDB(self):
        ''' 数据库连接关闭 '''
        self.conn.close()
