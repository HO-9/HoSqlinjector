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

dbms = dbck.check_dbms()
log.print_db_log(dbms)

if dbms != -1:
    error.error_based_sql(dbms)
else:
    #blind.blind_based_sql(dbms)
    print('b')
    time.time_based_sql(dbms)

# else:
# blind_sql
