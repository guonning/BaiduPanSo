#! /usr/bin/env python 
#coding=utf-8
#
import os
from Queue import Queue
import threading
import time
import urllib
from urlparse import *
from urlparse import urljoin
import redis
import urllib2
import time
import pymongo


conn = pymongo.MongoClient('localhost', 27017)
db = conn.BaiduPanSo


while True:
	time.sleep(2)
	print 'ren:'+str(db.ren.count())
	print 'ren to:'+str(db.ren.find({'fangwen':1}).count())
	print 'ren er:'+str(db.ren.find({'fangwen':2}).count())
	print 'ren ed:'+str(db.ren.find({'fangwen':3}).count())
	print 'url:'+str(db.url.count())
	print 'url to:'+str(db.url.find({'fangwen':1}).count())
	print 'url er:'+str(db.url.find({'fangwen':2}).count())
	print 'url ed:'+str(db.url.find({'fangwen':3}).count())
	print '-----------------\n'