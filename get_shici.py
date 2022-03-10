# -*- coding: utf-8 -*-

# 收集中华古诗词
# 本脚本仅用于个人学习
# 输入内容为 Markdown 文档

import os, sys, getopt
import re
from bs4 import BeautifulSoup
import requests
import time
import cgi

# https://www.shici123.cn/song/-------1
# https://www.shicimingju.com/paiming?p=2

class SCSpider():
    def get_html(self, url, method = "requests"):
        # config = self.read_config()
        my_cookie = ''

        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
        }

        # if config['cookie']:
        #     my_cookie = config['cookie']

        response = requests.get(url, headers = my_headers, cookies = my_cookie)
        response.encoding = 'utf-8'

        return response.text

    def get_pages_list(self):
        # 诗词排名链接列表
        page_list = []

        start_page = 'https://www.shicimingju.com/paiming?p=1'
        html = self.get_html(start_page)

        # 找出所有的页面导航链接
        soup = BeautifulSoup(html, 'html.parser')
        page_link = soup.find_all('div', attrs={ 'id':'list_nav_all' })
        page_link = page_link[0].find_all('a')

        print(page_link)
        # pass

sc = SCSpider()
sc.get_pages_list()
