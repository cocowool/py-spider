# -*- coding: utf-8 -*-
# 抓取空中课堂学习资料，整理并保存

# https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3

# 入口页面地址： https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3&_d=2020/10/25
import os, sys, getopt
import re
from bs4 import BeautifulSoup
import requests

class kzkt():
    # 通过requests方式获取网页内容
    def get_html(self, url, method = "requests"):
        # config = self.read_config()
        my_cookie = ''

        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'
        }

        # if config['cookie']:
        #     my_cookie = config['cookie']

        response = requests.get(url, headers = my_headers, cookies = my_cookie)

        return response.text

    # 遍历需要下载的视频和视频标题
    def parse_video(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        work_table = soup.find('span', attrs={'class':'content_table'}).contents
        print(work_table)
        pass

# 实例化
url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3&_d=2020/11/23"
dog = kzkt()
dog.parse_video(dog.get_html)
