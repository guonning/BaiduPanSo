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
import pymongo
import urllib2
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def get_url(url):
	try:
		request = urllib2.Request(url)
		return urllib2.urlopen(request,timeout=20).read()
	except Exception, e:
		raise e
# def get_count(url):
# 	data = re.findall(r'totalCount:"(.+?)"', get_url(url))
# 	if len(data) == 0:
# 		raise Exception('get_count err')
# 	return data[0]
# def get_count_all(uk):
# 	follow_count = get_count('http://pan.baidu.com/wap/share/home/followers?uk='+str(uk)+'&start=0')
# 	fan_count = get_count('http://pan.baidu.com/wap/share/home/fans?uk='+str(uk)+'&start=0')
# 	return follow_count, fan_count
def get_ren_info(url,neibie):
	try:
		data = get_url(url)
		matches = re.findall(r'parse\(\"(.+?)\"\),totalCount', data)
		if len(matches) == 0:
			raise Exception('get_ren_info err')
		data_decode = matches[0].decode("unicode_escape")
		jsondata = json.loads(data_decode)
		rens = []
		if len(jsondata) != 0:
			for i in jsondata:
				if neibie == 'follow':
					ren = {'fangwen':1,'uk':i['follow_uk'],'uname':i['follow_uname'],'avatar_url':i['avatar_url'],'intro':i['intro'],'fans_count':i['fans_count'],'follow_count':i['follow_count'],'pubshare_count':i['pubshare_count'],'album_count':i['album_count']}
				elif neibie == 'fans':
					ren = {'fangwen':1,'uk':i['fans_uk'],'uname':i['fans_uname'],'avatar_url':i['avatar_url'],'intro':i['intro'],'fans_count':i['fans_count'],'follow_count':i['follow_count'],'pubshare_count':i['pubshare_count'],'album_count':i['album_count']}
				rens.append(ren)
		return rens
	except Exception, e:
		raise e
def get_uk_all(url):
	try:
		url.index('followers')
		return get_ren_info(url,'follow')
	except ValueError:
		try:
			url.index('fans')
			return get_ren_info(url,'fans')
		except ValueError:
			raise ValueError('url str not found followers and fans')
def ren_mongo(uk, number):
	db.ren.update({'uk':uk}, {'$set':{'fangwen':number}})
def url_mongo(url, number):
	db.url.update({'url':url}, {'$set':{'fangwen':number}})
def drop():
	db.ren.drop()
	db.url.drop()
def init():
	ren_one = db.ren.find_one({'fangwen':1})
	if not ren_one:
		url = 'http://pan.baidu.com/wap/share/home/followers?uk=657260084&start=0'
		rens = get_uk_all(url)
		for i in rens:
			db.ren.save(i)
		url = 'http://pan.baidu.com/wap/share/home/followers?uk=657260084&start=24'
		rens = get_uk_all(url)
		for i in rens:
			db.ren.save(i)
	#queue
	for i in range(20):
		ren_one = db.ren.find_one({'fangwen':1})
		if ren_one:
			ren_queue.put(ren_one)
			ren_mongo(ren_one['uk'], 2)
		url_one = db.url.find_one({'fangwen':1})
		if url_one:
			url_queue.put(url_one)
			url_mongo(url_one['url'], 2)
def check():
	try:
		while True:
			if ren_queue.qsize() <20:
				ren_one = db.ren.find_one({'fangwen':1})
				if ren_one:
					ren_queue.put(ren_one)
					ren_mongo(ren_one['uk'], 2)
			if url_queue.qsize() <20:
				if url_one:
					url_queue.put(url_one)
					url_mongo(url_one['url'], 2)
	except Exception, e:
		raise Exception('??')
def deal_ren():
	name = threading.currentThread().getName()
	# = '1'
	while True:
		ren_one = ren_queue.get()
		if ren_one:
			uk = ren_one['uk']
			print "["+name+"号] "+str(uk)+"doing\n"
			try:
				follow_count = ren_one['follow_count']
				fans_count = ren_one['fans_count']
				print follow_count
				print fans_count
				for i in range(0,(24 if follow_count > 24 else follow_count),24):
					db.url.save({'url':'http://pan.baidu.com/wap/share/home/followers?uk='+str(uk)+'&start='+str(i),'fangwen':1})
				for j in range(0,(24 if fans_count > 24 else fans_count),24):
					db.url.save({'url':'http://pan.baidu.com/wap/share/home/fans?uk='+str(uk)+'&start='+str(j),'fangwen':1})
				ren_mongo(uk, 3)
			except Exception, e:
				#db.ren.update({'uk':uk}, {'$set':{'fangwen':1}})
				raise e
def deal_url():
	name = threading.currentThread().getName()
	#name = '1'
	while True:
		url_one = url_queue.get()
		if url_one:
			url = url_one['url']
			#db.url.update({'url':url}, {'$set':{'fangwen':2}})
			print "["+name+"号] doing\n"
			try:
				rens = get_uk_all(url)
				for i in rens:
					db.ren.save(i)
				url_mongo(url, 3)
			except Exception, e:
				#r.smove(key_url_mi,key_url_to,url)
				raise e
if __name__ == '__main__':
	#已经为ren表的uk和url表的url创建唯一索引
	#fangwen,1表示初始数据，2表示正在处理数据（意外数据会被保存在此），3表示已经计算数据
	#因为mongodb比较慢，所以引入队列
	#启动/opt/mongodb-3.0.7/bin/mongod --dbpath=/opt/mongodb-3.0.7/data/ --logpath=/opt/mongodb-3.0.7/log/mongo.log --fork
	#初始化drop(),init()
	# uks = ['842263796','321447710','2956110277','1566620287','436751272','3811108456','319707070','2435513896']
	#db.test.save({'name':'chen'})
	#db.test.update({'name':'chen'}, {'$set':{'name':'hahxa'}})
	#db.test.find({'name':'hahxa'})

	conn = pymongo.MongoClient('localhost', 27017)
	db = conn.BaiduPanSo
	ren_queue = Queue()
	url_queue = Queue()


	init()

	#queue
	worker=threading.Thread(target=check,name='name')
	worker.setDaemon(True)
	worker.start()
	#ren
	for i in range(2):
		worker=threading.Thread(target=deal_ren,name='ren_'+str(i+1))
		worker.start()
	#url
	for i in range(10):
		worker=threading.Thread(target=deal_url,name='url_'+str(i+1))
		worker.start()
