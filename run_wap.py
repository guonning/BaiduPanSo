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
def get_follow_url(url):
	try:
		data = get_url(url)
		matches = re.findall(r'parse\(\"(.+?)\"\),totalCount', data)
		if len(matches) == 0:
			raise Exception('get_follow_url err')
		jsondata = json.loads(matches[0].replace('\\',''))
		relist = []
		if len(jsondata) != 0:
			for dic in jsondata:
				relist.append(dic['follow_uk'])
		return relist
	except Exception, e:
		raise e
def get_fan_url(url):
	try:
		data = get_url(url)
		matches = re.findall(r'parse\(\"(.+?)\"\),totalCount', data)
		if len(matches) == 0:
			raise Exception('get_fan_url err')
		jsondata = json.loads(matches[0].replace('\\',''))
		relist = []
		if len(jsondata) != 0:
			for dic in jsondata:
				relist.append(dic['fans_uk'])
		return relist
	except Exception, e:
		raise e
def get_uk_url(url):
	try:
		url.index('followers')
		return get_follow_url(url)
	except Exception, e:
		try:
			url.index('fans')
			return get_fan_url(url)
		except Exception, e:
			raise Exception('url not found followers and fans')
def deal_ren():
	name = threading.currentThread().getName()
	while True:
		uk = r.spop(key_ren_to)
		if uk:
			print "["+name+"号] doing\n"
			try:
				follow_count, fan_count = get_count_all(uk)
				print follow_count
				print fan_count
				for i in range(0,int(follow_count),24):
					r.sadd(key_url_to,'http://pan.baidu.com/wap/share/home/followers?uk='+str(uk)+'&start='+str(i))
				for j in range(0,int(fan_count),24):
					r.sadd(key_url_to,'http://pan.baidu.com/wap/share/home/fans?uk='+str(uk)+'&start='+str(j))
				r.sadd(key_ren_ed,uk)
			except Exception, e:
				r.sadd(key_ren_to,uk)
				print e
def deal_url():
	name = threading.currentThread().getName()
	while True:
		url = r.spop(key_url_to)
		try:
			print "["+name+"号] doing\n"
			data = get_uk_url(url)
			for i in data:
				r.sadd(key_ren_to,i)
			r.sadd(key_url_ed,url)
		except Exception, e:
			r.sadd(key_url_to,url)
			print e
if __name__ == '__main__':
	key_ren_to = 'redis_pan_ren_to'
	key_ren_ed = 'redis_pan_ren_ed'
	
	key_url_to = 'redis_pan_url_to'
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
	#url
	worker=threading.Thread(target=deal_url,name='url_1')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_2')
	worker.start()
	worker=threading.Thread(target=deal_url,name='url_3')
	worker.start()
