#! /usr/bin/env python
#coding=utf-8
#
import redis

key_ren_to = 'redis_pan_ren_to'
key_ren_mi = 'redis_pan_ren_mi'
key_ren_ed = 'redis_pan_ren_ed'
key_ren_info = 'redis_pan_ren_info'

key_url_to = 'redis_pan_url_to'
key_url_mi = 'redis_pan_url_mi'
key_url_ed = 'redis_pan_url_ed'
r =  redis.Redis(host='localhost', port=6379)

# print r.smembers(key_to)
# print r.smembers(key_mi)
# print r.smembers(key_ed)
# print r.smembers(key_no)

r.delete(key_ren_to)
r.delete(key_ren_mi)
r.delete(key_ren_ed)
r.delete(key_ren_info)
r.delete(key_url_to)
r.delete(key_url_mi)
r.delete(key_url_ed)

print r.smembers(key_ren_to)
print r.smembers(key_ren_mi)
print r.smembers(key_ren_ed)
print r.smembers(key_ren_info)
print r.smembers(key_url_to)
print r.smembers(key_url_mi)
print r.smembers(key_url_ed)

