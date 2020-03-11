# -*- coding: utf-8 -*-

import os
import configparser
import random
from utils.logger import LoggerUtil

logger = LoggerUtil().get_log


project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)).replace('\\','/')
config_dir = os.path.join(project_path, "config").replace('\\','/')
config_path  = os.path.join(config_dir, "config.ini").replace('\\','/')

logger.info("project path : {project_path}".format(project_path = project_path))
logger.info("config dir : {config_dir}".format(config_dir = config_dir))
logger.info("config path : {config_path}".format(config_path = config_path))

def get_user_agent():
    config = configparser.ConfigParser()
    config.read(config_path, encoding = "utf-8")
    userAgents = config.items("User-Agent")
    return userAgents

def random_user_agent():
    vlues = get_user_agent()
    return random.choice(vlues)[1]

def get_config():
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config

config = get_config()

class ConfigParser(object):
    config_dic = {}

    @staticmethod
    def get_config(sector, item):
        value = None

        try:
            cf = configparser.ConfigParser()
            cf.read(config_path, encoding='utf8')
            value = cf.get(sector, item)
            ConfigParser.config_dic = value
        except KeyError:
            pass
        finally:
            return value