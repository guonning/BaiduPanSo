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

key_ren_to = 'redis_pan_ren_to'
key_ren_mi = 'redis_pan_ren_mi'
key_ren_ed = 'redis_pan_ren_ed'
key_ren_info = 'redis_pan_ren_info'

key_url_to = 'redis_pan_url_to'
key_url_mi = 'redis_pan_url_mi'
key_url_ed = 'redis_pan_url_ed'


r =  redis.Redis(host='localhost', port=6379)

while True:
	time.sleep(2)
	print 'key_ren_to:'+str(r.scard(key_ren_to))
	print 'key_ren_mi:'+str(r.scard(key_ren_mi))
	print 'key_ren_ed:'+str(r.scard(key_ren_ed))
	print 'key_ren_info:'+str(r.scard(key_ren_info))
	print 'key_url_to:'+str(r.scard(key_url_to))
	print 'key_url_mi:'+str(r.scard(key_url_mi))
	print 'key_url_ed:'+str(r.scard(key_url_ed))
	print '-----------------\n'




