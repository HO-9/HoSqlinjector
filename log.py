# -*- coding: utf-8 -*-
import logging

mylogger = logging.getLogger()
mylogger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(levelname)s] - %(message)s')
stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
mylogger.addHandler(stream_hander)


def print_db_log(msg):
    msg  = "It's database looks like '"+msg+"'"
    mylogger.info(msg)

