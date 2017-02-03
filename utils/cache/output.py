import pymysql
import logging
import sys
from .pak import *
from utils.consts import const


class Output(object):
    """
    输出的抽象类
    """

    def output(self, catchedpak):
        raise NotImplementedError


class Database(Output):
    """
    数据库的实例
    """

    def __init__(self):
        self.connection = pymysql.connect(**const.DBCONF)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            'CREATE TABLE cachedata.catchedinfo (\n'
            '`ip` varchar(30) NOT NULL,\n'
            '`querytime` datetime NOT NULL,\n'
            '`type` varchar(30) DEFAULT NULL,\n'
            ') ENGINE=MyISAM DEFAULT CHARSET=utf8\n'
        )

    def output(self, catchedpak):
        self.cursor.execute(
            ('insert into {table}\n'
             '(`ip`, `time`, `type`)\n'
             'VALUES (\'{ip}\', \'{time}\', \'{type}\')'
             ).format(
                table=cacheconf.CATCHEDTABLE,
                ip=catchedpak.ip,
                time=catchedpak.time,
                type='cache'
            )
        )


class Logger(Output):
    """
    日志的实例
    """

    def __init__(self):
        self.logger = logging.getLogger('logger')
        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def output(self, catchedpak):
        self.logger.info('ip: ' + str(catchedpak.ip) + ', time: ' + str(catchedpak.time))


class FileLogger(Output):
    """
    文件日志的实例
    """

    def __init__(self):
        self.logger = logging.getLogger('filelogger')
        self.logger.addHandler(logging.FileHandler(cacheconf.FILELOG_PATH))
        self.logger.setLevel(logging.INFO)

    def output(self, catchedpak):
        self.logger.info('ip: ' + str(catchedpak.ip) + ', time: ' + str(catchedpak.time))
