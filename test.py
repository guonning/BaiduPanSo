#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import redis
import json


r =  redis.Redis(host='localhost', port=6379)

def get_pro():
	try:
		pro = r.spop('redis_pan_pro')
		if pro == None:
			try:
				pros =  urllib2.urlopen('http://chenapi.sinaapp.com/index.php/api').read()
				for i in json.loads(pros):
					r.sadd('redis_pan_pro',i)
				return get_pro()
			except Exception, e:
				raise e
		else:
			return pro
	except Exception, e:
		raise e

def url_user_agent(url):
	try:
		try:
			pro = get_pro()
		except Exception, e:
			raise Exception('get pro_http err')
		proxy = {'http': pro}
		proxy_support = urllib2.ProxyHandler(proxy)
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)
		i_headers = {
			'Host':'www.baidu.com',
			'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
			'Referer' : 'http://www.baidu.com',
			'Connection' : 'keep-alive'
		}
		req = urllib2.Request(url,headers=i_headers)
		return urllib2.urlopen(req,timeout=20).read()
	except Exception, e:
		raise e

print url_user_agent('http://pan.baidu.com/pcloud/friend/getfanslist?query_uk=3154767138&limit=24&start=0')
