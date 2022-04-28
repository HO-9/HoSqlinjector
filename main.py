#-*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse
import blind_sql as blind
import error_sql as error
import setting as set



dbms = set.check_dbms()

if dbms != -1:
    error.error_based_sql(dbms)
else:
    blind.blind_based_sql(dbms)

#else:
    #blind_sql