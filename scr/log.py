#-*- coding:utf-8 -*-
# @Author : Dummerfu
# @Time : 2020/10/29 18:54
'''
生成日志文件
'''
import logging
from logging import handlers
import os
import time
class Loggers(object):
    def __init__(self,encoding=None,level=logging.INFO):
        path=os.path.abspath('..')
        path=os.path.join(path,'log')
        self.encoding=encoding
        self.level=level

        if not os.path.exists(path):
            os.mkdir(path)


        __time__ = time.strftime('%Y_%m_%d_%H_%M',time.localtime(time.time()))

        self.logger = logging.getLogger('log')

        self.logger_name=os.path.join(path,'default')

        # 防止不正确调用 造成handle重复
        while self.logger.hasHandlers():
            for i in self.logger.handlers:
                self.logger.removeHandler(i)

        self.logger.setLevel(self.level)

        fh=logging.handlers.TimedRotatingFileHandler(filename=self.logger_name,when="S",interval=1,backupCount=50,encoding='utf-8')

        formater = logging.Formatter('%(asctime)s [%(filename)s] <line:%(lineno)d> (%(levelname)s) : %(message)s')
        fh.setFormatter(formater)

        self.logger.addHandler(fh)

        # 初始信息
        # self.logger.info(path)


if __name__ == '__main__':
    logger=Loggers()
    # try:
    #     while 1:
    #         print(aaa)
    # except Exception as e:
    #     logger.logger.exception(e)