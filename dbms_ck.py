# -*- coding: utf-8 -*-
import httplib
import urllib
from urlparse import urlparse
import sys
import time
import argparse
import error_sql as error
import socket
import setting as set
import threading
import log as log
import time


#3306                    -> MySQL,MariaDB
#1433,1434               -> MS-SQL
#1521,1522               -> Oracle


db_port = [3306,1521,1522,1433,1434]
open_port = 0
db = {"mysql":3306, "mssql":[1433,1434], "oracle":[1521,1522]}

#def check_name():

def error_db_check():
    ck_dbms = set.httpreq("'")

    if ck_dbms.find('MySQL') != -1:
        cn_dbms = 'mysql'
        return cn_dbms

    elif ck_dbms.find('mssql') != -1:
        cn_dbms = 'mssql'
        return cn_dbms

    elif ck_dbms.find('ORA') != -1:
        cn_dbms = 'oracle'
        return cn_dbms

    else:
        print "[Info] Couldn't Assume database"
        return -1

#def blind_db_check():
#    a = set.httpreq("1 and substr(@@version,1,1)=5-- ")
#    print(a)

#def time_db_check():
#    set.caller_time_httpreq("' and select count(*) from information_schema.tables tab1,information_schema.tables tab2,information_schema.tables tab3")
#    #set.httpreq("' and select count(*) from information_schema.tables tab1,information_schema.tables tab2,information_schema.tables tab3")


def scan_check(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(4)
    try:
        global open_port
        con = sock.connect((set.domain, port))
        open_port = port
        con.close()

    except:
        pass



def check_dbms():
    for db_arr in range(0,len(db_port)):
        #print(db_port[db_arr])
        time.sleep(0.1)
        thread = threading.Thread(target=scan_check, kwargs={"port": db_port[db_arr]})
        thread.start()

    # Modifying Open port number to DbName
    # 만약 service 두개 이용하면 맨 위에서 걸러 질 수가 있음 염두해서 다시 짜야 됨 일단 초안임


    #Scan 후 포트에 대한 응답값이 없으면 error 기반의 체크 시작
    #이후 error를 통해서 DB를 알아내면 error 기반 Injection시작
    #error 값을 넣어줬는데 동일한 반응 보일경우 Time based Injection 시도

    log.debugging("Check Port: "+str(open_port))
    if open_port == db["mysql"]:
        return "mysql"
    elif open_port in db["mssql"]:
        return "mssql"
    elif open_port in db["oracle"]:
        return "oracle"
    else:
        error_db_check()



