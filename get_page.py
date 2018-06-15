# 介绍三种不同方式获取单个页面的方法

import urllib
# from urllib.request import request
from urllib.urlopen import urlopen
# import urllib2
import requests

# 使用 urllib 方式获取
response = urllib.request.urlopen('http://www.baidu.com')
# read() 读取的是服务器的原始返回数据 decode() 后会进行转码
print(response.read().decode())

# 使用 requests 方式获取
# request 模块相比
resp = requests.get('http://www.baidu.com')
print(resp)
print(resp.text)

# 使用带参数的接口访问
tencent_api = "http://qt.gtimg.cn/q=sh601939"

response = urllib.request.urlopen(tencent_api)
# read() 读取的是服务器的原始返回数据 decode() 后会进行转码
print(response.read())

resp = requests.get(tencent_api)
print(resp)
print(resp.text)
