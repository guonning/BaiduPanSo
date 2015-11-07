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
import random
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def suiji():
	string = ''
	return string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 26)).replace(' ','')

def test():
	a = []
	return a
def up():
	name = threading.currentThread().getName()
	ren_one = db.test.find_one({'fangwen':1})
	db.test.update({'name':ren_one['name']}, {'$set':{'fangwen':'2'}})
	print name+'update 1111111111111111111111111111111111111111111111111\n'
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

	data = test()
	for i in data:
		print i
