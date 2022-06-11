# -*- coding: utf-8 -*-
import logging

mylogger = logging.getLogger()
formatter = logging.Formatter('[%(levelname)s] - %(message)s')
stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
mylogger.addHandler(stream_hander)


def print_db_log(msg):
    mylogger.setLevel(logging.INFO)
    msg  = "It's database looks like '"+msg+"'"
    mylogger.info(msg)

def print_based_log(msg):
    mylogger.setLevel(logging.INFO)
    msg = msg+" is available and it is in processing"
    mylogger.info(msg)

def debugging(msg):
    mylogger.setLevel(logging.DEBUG)
    mylogger.debug(msg)

def info(msg):
    mylogger.setLevel(logging.INFO)
    mylogger.info(msg)