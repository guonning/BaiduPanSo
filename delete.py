#! /usr/bin/env python
#coding=utf-8
#
import pymongo
conn = pymongo.MongoClient('localhost', 27017)
db = conn.BaiduPanSo
db.ren.drop()
db.url.drop()

