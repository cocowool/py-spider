# 介绍三种不同方式获取单个页面的方法

import urllib
# import urllib2
import requests

# 使用 urllib 方式获取
response = urllib.request.urlopen('http://www.baidu.com')
print(response.read())

# 使用 requests 方式获取
resp = requests.get('http://www.baidu.com')

print(resp)
print(resp.text)
