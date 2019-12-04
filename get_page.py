#coding=utf-8
# 介绍三种不同方式获取单个页面的方法

import os
import sys
import importlib
importlib.reload(sys)
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.path.append(os.getcwd())

import urllib3
import urllib3.request
# import urllib.request
# # from urllib.request import request
# from urllib3 import urlopen

# 使用 urllib 方式获取
response = urllib3.request.urlopen('http://www.baidu.com/s?ie=utf-8&wd=国双科技')
# 打印服务器返回的状态码
print(response.code)
# read() 读取的是服务器的原始返回数据 decode() 后会进行转码
print(response.read().decode('utf-8'))


# # import urllib2
# import requests


# # 使用 requests 方式获取
# # request 模块相比
# resp = requests.get('http://www.baidu.com')
# # 打印服务器返回的状态码
# print(resp.status_code)
# print(resp)
# print(resp.text)

# # HTTP 是基于请求和响应的工作模式，urllib.request 提供了一个 Request 对象来代表请求，因此上面的代码也可以这么写
# req = urllib.request.Request('http://www.baidu.com')
# with urllib.request.urlopen(req) as response:
#     print(response.read())


# # 使用带参数的接口访问
# tencent_api = "http://qt.gtimg.cn/q=sh601939"

# response = urllib.request.urlopen(tencent_api)
# # read() 读取的是服务器的原始返回数据 decode() 后会进行转码
# print(response.read())

# resp = requests.get(tencent_api)
# print(resp)
# print(resp.text)


