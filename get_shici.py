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
        page_prefix = 'https://www.shicimingju.com'
        html = self.get_html(start_page)

        # 找出所有的页面导航链接
        soup = BeautifulSoup(html, 'html.parser')
        page_link = soup.find_all('div', attrs={ 'id':'list_nav_all' })
        page_link = page_link[0].find_all('a')

        m = 0
        for i in page_link:
            page_list.append( page_prefix + i.get('href') )
            # print( i.get('href') )
            # print(i)

        return page_list
        # print(page_list)
        # pass

    # 解析列表页，获取具体诗词列表
    def get_poem_list(self, page_list):
        shici_list = []
        href_list = []
        page_prefix = 'https://www.shicimingju.com'

        for i in page_list:
            html = self.get_html(i)
            shici  = BeautifulSoup(html, 'html.parser')
            shici_link = shici.find_all('div', attrs={'class':'shici_list_main'})
            for j in shici_link:
                # j = j.find_all('h3')
                # print(j)
                # j = BeautifulSoup(j, 'html.parser')
                # j = j.find('h3').find('a').get('href')
                href_list.append( page_prefix + j.find('h3').find('a').get('href') )

            shici_list.append(shici_link)
            # print(shici_link)
            # print(html)
        

        # for i in shici_list:
            # print(i)
            # href_list.append( i.find_all('h3').get('href') )

        # print(href_list)
        # return href_list
        return href_list

    # 根据诗词列表页，解析每个诗词内容
    # 构建一个诗词的消息体，方便保存为文件时使用
    # poem.title / poem.author / poem.dynasty / poem.fulltext / poem.description
    def get_poem_detail(self, poem_link):
        html = self.get_html(poem_link)
        print(html)
        pass

    # 将诗词内容保存为 Markdown 文件
    def save_poem_2_md(self):
        pass

sc = SCSpider()
# page_list = sc.get_pages_list()
# shici_list = sc.get_poem_list(page_list)

test_poem_link = 'https://www.shicimingju.com/chaxun/list/38123.html'
sc.get_poem_detail(test_poem_link)

# poem_detail = sc.get_poem_detail(shici_list)

# print(shici_list)