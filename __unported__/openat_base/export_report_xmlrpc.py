#!/usr/bin/python

import xmlrpclib
import os
import sys
import csv
import codecs


dbname = 'austriadb_01'
host = 'localhost'
port = 41069
username = 'admin'
pwd = ''

obj = 'sale.order'
report = 'report.sale.order.openat'
outfilename = '/opt/openerp/ope-7.0-41069/report.odt'

sock_common = xmlrpclib.ServerProxy ('http://%s:%d/xmlrpc/common' % (host, port))
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://%s:%d/xmlrpc/object' % (host, port))

# get all ids of the object
ids = sock.execute(dbname, uid, pwd, obj, 'search', [])
print ids

context = {}
context['model'] = obj
context['ids'] = ids
print context

# call the function
res = sock.execute(dbname, uid, pwd, 'ir.cron', 'openat_print_report', ids, report, outfilename, context)
