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
import json
import re

def get_url(url):
	try:
		request = urllib2.Request(url)
		return urllib2.urlopen(request,timeout=20).read()
	except Exception, e:
		raise e
def get_count(url):
	data = re.findall(r'totalCount:"(.+?)"', get_url(url))
	if len(data) == 0:
		raise Exception('get_count err')
	return data[0]
def get_count_all(uk):
	follow_count = get_count('http://pan.baidu.com/wap/share/home/followers?uk='+str(uk)+'&start=0')
	fan_count = get_count('http://pan.baidu.com/wap/share/home/fans?uk='+str(uk)+'&start=0')
	return follow_count, fan_count
def get_ren_info(url,neibie):
	try:
		data = get_url(url)
		matches = re.findall(r'parse\(\"(.+?)\"\),totalCount', data)
		if len(matches) == 0:
			raise Exception('get_ren_info err')
		data_decode = matches[0].decode("unicode_escape")
		jsondata = json.loads(data_decode)
		rens = []
		uks = []
		if len(jsondata) != 0:
			for dic in jsondata:
				rens.append(dic)
				uks.append(dic[neibie])
		return rens, uks
	except Exception, e:
		raise e
def get_uk_all(url):
	try:
		url.index('followers')
		return get_ren_info(url,'follow_uk')
	except Exception, e:
		try:
			url.index('fans')
			return get_ren_info(url,'fans_uk')
		except Exception, e:
			raise Exception('url not found followers and fans')
def deal_ren():
	name = threading.currentThread().getName()
	while True:
		uk = r.srandmember(key_ren_to)
		if uk:
			r.smove(key_ren_to,key_ren_mi,uk)
			print "["+name+"号] doing\n"
			try:
				follow_count, fan_count = get_count_all(uk)
				print follow_count
				print fan_count
				for i in range(0,long(follow_count),24):
					if not r.sismember(key_ren_mi,i) and not r.sismember(key_ren_ed,i):
						r.sadd(key_url_to,'http://pan.baidu.com/wap/share/home/followers?uk='+str(uk)+'&start='+str(i))
				for j in range(0,long(fan_count),24):
					if not r.sismember(key_ren_mi,j) and not r.sismember(key_ren_ed,j):
						r.sadd(key_url_to,'http://pan.baidu.com/wap/share/home/fans?uk='+str(uk)+'&start='+str(j))
				r.smove(key_ren_mi,key_ren_ed,uk)
			except Exception, e:
				r.smove(key_ren_mi,key_ren_to,uk)
				print e
def deal_url():
	name = threading.currentThread().getName()
	while True:
		url = r.srandmember(key_url_to)
		if url:
			r.smove(key_url_to,key_url_mi,url)
			print "["+name+"号] doing\n"
			try:
				rens, uks = get_uk_all(url)
				for i in rens:
					if not r.sismember(key_url_mi,i) and not r.sismember(key_url_ed,i):
						r.sadd(key_ren_info,i)
				for j in uks:
					if not r.sismember(key_url_mi,i) and not r.sismember(key_url_ed,i):
						r.sadd(key_ren_to,j)
				r.smove(key_url_mi,key_url_ed,url)
			except Exception, e:
				r.smove(key_url_mi,key_url_to,url)
				print e
if __name__ == '__main__':
	key_ren_to = 'redis_pan_ren_to'
	key_ren_mi = 'redis_pan_ren_mi'
	key_ren_ed = 'redis_pan_ren_ed'
	key_ren_info = 'redis_pan_ren_info'
	
	key_url_to = 'redis_pan_url_to'
	key_url_mi = 'redis_pan_url_mi'
	key_url_ed = 'redis_pan_url_ed'
	
	num_threads=2

	uks = ['842263796','321447710','2956110277','1566620287','436751272','3811108456','319707070','2435513896']
	#uks = ['657260084']

	r =  redis.Redis(host='localhost', port=6379)

	#chushuhua
	is_uk = r.srandmember(key_ren_to)
	if not is_uk:
		for uk in uks:
			r.sadd(key_ren_to,uk)
	#ren
	worker=threading.Thread(target=deal_ren,name='ren_1')
	worker.start()
	worker=threading.Thread(target=deal_ren,name='ren_2')
	worker.start()
	worker=threading.Thread(target=deal_ren,name='ren_3')
	worker.start()
	worker=threading.Thread(target=deal_ren,name='ren_4')
	worker.start()
	#url
	worker=threading.Thread(target=deal_url,name='url_1')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_2')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_3')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_4')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_5')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_6')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_7')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_8')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_9')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_10')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_11')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_12')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_13')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_14')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_15')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_16')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_17')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_18')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_19')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_20')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_21')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_22')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_23')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_24')
	worker.start()
