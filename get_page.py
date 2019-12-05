# coding=utf-8
# 获取单个页面的内容

import re
import urllib.request
import ssl

import os
import sys
import importlib
importlib.reload(sys)
import codecs
import requests

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.path.append(os.getcwd())

# 使用urllib方式获取页面内容
def getHtml(url, header = ""):
    request = urllib.request.Request(url, headers = header )
    page = urllib.request.urlopen(request)
    html = page.read().decode('utf-8')
    return html

# 使用Requests方式获取页面内容
# Requests 是更高阶的包装方式，使用起来更简单
def getHtml_Requests(url):
    response = requests.get(url)
    return response.text

ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://www.baidu.com/s?wd=kubernetes&tn=84053098_3_dg&ie=utf-8'
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}

print("Get HTML Via urllib")
html = getHtml(url, header)
print(html)

print("Get HTML Via Requests")
html = getHtml_Requests(url)
print(html)