# -*- coding: utf-8 -*-
# 抓取空中课堂学习资料，整理并保存。

# @TODO 设置一个DEBUG变量，DEBUG开启的时候，只打印需要下载的连接，保存的目标地址以及文件名，但不执行真正的下载

# https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3

# 入口页面地址： https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3&_d=2020/10/25
import os, sys, getopt
import re
from bs4 import BeautifulSoup
import requests
import time
import cgi

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

    # 将内容保存为文件
    def save_file(self, contents, file_name):
        with open(file_name, "wb") as file_obj:
            file_obj.write(contents)
        pass

    # 请求视频地址并保存为文件
    def save_video(self, video_url, file_name):
        start_time = time.time()
        chunk_size = 4096

        response = requests.head(url=video_url)
        headers = {}

        # 初始化当前下载完成的文件大小
        size = 0

        try:
            total_file_size = int(response.headers['Content-Length'])
        except Exception as e:
            print("get header error")
            print(e.args)

        print( total_file_size )
        print('Start download, [File size]:{size:.2f} MB'.format(size = total_file_size / 1024))

        if not os.path.exists(file_name):
            with open(file_name, 'ab+') as f:
                pass
        
        file_size = os.path.getsize(file_name)
        download_flag = True
        while download_flag:
            try:
                file_size = os.path.getsize(file_name)
                headers['Range'] = 'bytes=%d-' % file_size
                response = requests.get(url=video_url, headers=headers, stream=True, timeout=20)
                with open(file_name, 'ab+') as f:
                    # 请求没有被显示的关闭，可能会有性能问题
                    for chunk in response.iter_content(chunk_size = chunk_size):
                        if response.status_code == 206:
                            if chunk:
                                f.write(chunk)
                                size += len(chunk)
                                print('\r' + '[Download progress]:%s%.2f%\n' % ('>' * int(size * 50 / total_file_size), float(size/total_file_size*100)) )
                        elif os.path.getsize(file_name) >= total_file_size:
                            download_flag = False
                            return file_name
                        else:
                            print("program sleep")
                            time.sleep(3)
                            break
            except Exception as e:
                print("download error:")
                print(e.args)

        end_time = time.time()

        print('Download completed!, times: %.2f seconds' % (end_time - start_time))

    # 下载页面中的视频及课件
    def download_video(self, url, save_folder):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取课程名称
        lesson_name = soup.find('span', attrs = {'id':'album_lesson_name'})
        print(lesson_name.text)

        # 获取视频资源的链接地址
        video_url = re.search(r'videourl="(.*)"', response.text).group(1).strip()

        # 判断并创建文件夹
        if os.path.exists(save_folder):
            self.save_video( video_url, save_folder + "/" + lesson_name.text + ".mp4" )
        else:
            os.makedirs(r"" + save_folder)
            self.save_video( video_url, save_folder + "/" + lesson_name.text + ".mp4" )

        # print(response.text)
        # print(soup.find_all('script'))


        # print(soup.find_all('a', attrs={'class':'file_view_list'}))
        # file_name = '1123.ppt'
        # ppt_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=872462"
        # file_res = requests.get(ppt_url)
        pass

    # 下载视频页面的文件
    def download_file(self, file_url, save_folder):
        response = requests.head(url=file_url)
        print(response.headers)
        # print(response.headers['Content-Disposition'].encode('utf-8'))
        # print(type(response.headers['Content-Disposition']))
        value, params = cgi.parse_header( response.headers['Content-Disposition'] )
        # print(value)
        print(params['filename'].encode('ISO-8859-1').decode('utf8'))
        pass

    # 解析课程表，将一个学习的课程表对应的链接都获取到
    def parse_table(self, table_start_url):
        html = self.get_html(table_start_url)

        # 遍历需要下载的视频和视频标题
        soup = BeautifulSoup(html, 'html.parser')
        work_table = soup.find_all('table', attrs={'class':'content_table', 'grade' : '3'})

        for item in work_table:

            i = 0
            j = 0
            # 表格为6行6列，国庆期间表格较为特殊，最大表格为7行7列
            table_data = [ ['' for m in range(7)] for n in range(7) ]
            print(table_data)
            
            trs = item.find_all('tr')
            for tr in trs:
                cells = tr.find_all('th')
                if not cells:
                    cells = tr.find_all('td')
                for cell in cells:
                    table_data[i][j] = cell.get_text()
                    print(j)
                    # print(table_data)
                    j = j + 1
                print(i)
                i = i + 1
                j = 0

            print(table_data)
            # chinese_td = item.find_all('td', attrs={'class':'content_table_td'})

            # for sub_item in chinese_td:
            #     # print(sub_item)
            #     print("Table:" + str(i) + ", Td: " + str(j))
            #     j = j + 1
            # i = i + 1
            # print(item)

        print(len(work_table))
        pass


# 保存路径规划
# teaching_resource / YYYY-MM-DD-Name / xxxx.video,ppt,docx

# 实例化
course_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3"
video_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/weike/0bf79a3ba787b32a7ed2df8844e7dd8e.html?grade_id=3&subject_id=1"
# file_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=908001"
file_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=872507"

table_start_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3"

dog = kzkt()
dog.parse_table(table_start_url)

# dog.parse_video(dog.get_html(url))
# dog.download_video(video_url, 'videos')
# dog.download_file(file_url, 'videos')