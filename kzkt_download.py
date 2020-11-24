# -*- coding: utf-8 -*-
# 抓取空中课堂学习资料，整理并保存。

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
        # print(type(html))
        soup = BeautifulSoup(html, 'html.parser')
        work_table = soup.find_all('table', attrs={'class':'content_table', 'grade' : '3'})
        print(len(work_table))
        pass

    # 下载页面中的视频及课件
    def download_video(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # print(response.text)
        # print(soup.find_all('video'))
        print(soup.find_all('a', attrs={'class':'file_view_list'}))

        file_name = '1123.ppt'
        ppt_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=872462"
        file_res = requests.get(ppt_url)
        with open(file_name, "wb") as ppt:
            ppt.write(file_res.content)

        pass

# 实例化
course_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3&_d=2020/11/23"
video_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/weike/0bf79a3ba787b32a7ed2df8844e7dd8e.html?grade_id=3&subject_id=1"
dog = kzkt()
# dog.parse_video(dog.get_html(url))

dog.download_video(video_url)