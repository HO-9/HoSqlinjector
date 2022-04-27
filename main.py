#-*- coding: utf-8 -*-

import httplib
import urllib
from urlparse import urlparse
import sys
import argparse

import error_sql
import error_sql as error
import setting as set



dbms = set.check_dbms()

if dbms != -1:
    error_sql.error_based_sql(dbms)


#else:
    #blind_sql