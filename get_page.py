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

def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html

def getHtml_Requests(url):
    response = requests.get(url)
    return response.text

ssl._create_default_https_context = ssl._create_unverified_context
url = 'https://www.baidu.com/s?ie=utf-8&wd=kubernetes'
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"}

print("Get HTML Via urllib")
html = getHtml(url)
print(html)

print("Get HTML Via Requests")
html = getHtml_Requests(url)
print(html)