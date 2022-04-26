#-*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse
import error_sql as error
import setting as set



ck_dbms =   set.httpreq("'")
cn_dbms = ''

if ck_dbms.find('MySQL') != -1:
    cn_dbms = 'MYSQL'
    print "[Info] It's database looks like '"+cn_dbms+"'"
    error.error_based_sql()

elif ck_dbms.find('mssql') != -1:
    cn_dbms = 'MSSQL'
    print "[Info] It's database looks like '"+cn_dbms+"'"

elif ck_dbms.find('ORA') != -1:
    cn_dbms = 'MySQL'
    print "[Info] It's database looks like '"+cn_dbms+"'"

else:
    print "[Info] Couldn't Assume database"
