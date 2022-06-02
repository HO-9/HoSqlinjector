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
from dbms_ck import finger_scan,finger_error
import log as log

dbms = dbck.check_dbms()
log.print_db_log(dbms)

#if dbms != -1:
#    time.time_based_sql(dbms)

print(finger_scan)

#############문제점 ...
#finger_scan의 전역변수가 말을 안들음
#전역변수로 해서 값을 변경하고 다른 파일에서 임포트해서 쓰는 경우 원래 값으로 변경이 되어있음
#심지어 원래 파일에서 전역변수 값 변경하는 것도 이상함

if finger_scan and finger_error:
    log.print_based_log("Time Based & Error Based Injection")
    error.error_based_sql(dbms)

elif finger_scan:
    print("b")
    log.print_based_log("Time Based Injection")
    time.time_based_sql(dbms)

elif finger_error:
    log.print_based_log("Error Based Injection")
    error.error_based_sql(dbms)

elif dbms == -1:
    print("c")
    log.print_based_log("Time Based Injection")
    time.time_based_sql(dbms)

# else:
# blind_sql
