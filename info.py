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


data = db.ren.find()
url = db.url.find()
i=0
while True:
	time.sleep(2)
	print data[i]
	print url[i]
	i+=1





