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

#3306                    -> MySQL,MariaDB
#1433,1434               -> MS-SQL
#1521,1522               -> Oracle
#5432                    -> PostgreSQL
#27017,27018,27019,28017 -> MongoDB

db_port = [3306,1521,1522,1433,1434,5432,8629,27017,27018,27019,28017]

def error_db_check():
    ck_dbms = set.httpreq("'")

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

def nc_db_check():
    try:
        for i in range(0,len(db_port)):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (set.domain,db_port[i])
            print(server_address)
            sock.connect(server_address)
            print(sock.recv(1000))
            sock.close()
    except:



def check_dbms():
    nc_db_check()
    error_db_check()