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
import urllib.parse

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
        response.encoding = 'utf-8'

        return response.text

    # 将内容保存为文件
    def test_save_file(self, contents, file_name):
        with open(file_name, "wb") as file_obj:
            file_obj.write(contents)
        pass

    # 请求视频地址并保存为文件
    def download_file(self, file_url, file_name):
        start_time = time.time()
        chunk_size = 4096

        response = requests.head(url=file_url)
        headers = {}

        # 初始化当前下载完成的文件大小
        size = 0

        try:
            total_file_size = int(response.headers['Content-Length'])
        except Exception as e:
            print("get header error")
            print(e.args)

        print( 'File Name : ' + file_name )
        print('Start download, [File size]:{size:.2f} MB'.format(size = total_file_size / 1024 / 1024))

        if not os.path.exists(file_name):
            with open(file_name, 'ab+') as f:
                pass
        
        file_size = os.path.getsize(file_name)
        download_flag = True
        while download_flag:
            try:
                file_size = os.path.getsize(file_name)
                headers['Range'] = "bytes=%s-%s" % (file_size, total_file_size)
                headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
                response = requests.get(url=file_url, headers=headers, stream=True, timeout=20)
                with open(file_name, 'ab+') as f:
                    # 请求没有被显示的关闭，可能会有性能问题
                    for chunk in response.iter_content(chunk_size = chunk_size):
                        if response.status_code == 206:
                            if chunk:
                                f.write(chunk)
                                size += len(chunk)
                                # print('\r' + '[ Download progress ]:%s%.2f%\n' % ('>' * int(size * 50 / total_file_size), float(size/total_file_size*100)) )
                        elif os.path.getsize(file_name) >= total_file_size:
                            download_flag = False
                            return file_name
                        else:
                            print("program sleep")
                            time.sleep(3)
                            break
            except Exception as e:
                print(file_url)
                print("download error:")
                print(e)
                # print(Argument)

        end_time = time.time()

        print('Download completed!, times: %.2f seconds' % (end_time - start_time))

    # 下载页面中的视频及课件
    def download_files(self, url, save_folder):
        save_folder_prefix = "./teaching_resource/"
        save_folder = save_folder_prefix + save_folder

        # 判断并创建文件夹
        if not os.path.exists(save_folder):
            os.makedirs(r"" + save_folder)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取课程名称
        lesson_name = soup.find('span', attrs = {'id':'album_lesson_name'})
        print(lesson_name.text)

        # 获取视频资源的链接地址
        video_url = re.search(r'videourl="(.*)"', response.text).group(1).strip()

        print("Video Url : " + video_url)
        self.download_file( video_url, save_folder + "/" + lesson_name.text + ".mp4" )

        # print(response.text)
        # print(soup.find_all('script'))

        # print(soup.find_all('a', attrs={'class':'file_view_list'}))
        # file_name = '1123.ppt'
        # ppt_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=872462"
        # file_res = requests.get(ppt_url)

        # 获取需要下载的文件列表
        file_lists = soup.find_all('div', attrs = {'class':'recourse_item'})
        for f in file_lists:
            print("File name:" + f.get_text().strip())
            print("File Url:" + f.a['href'])
            self.save_file( "https://video.cache.bdschool.cn" + f.a['href'], save_folder)
        pass

    # 下载保存视频页面的文件
    def save_file(self, file_url, save_folder):
        # file_url_prefix = 'https://cache.bdschool.cn'
        file_url_prefix = ''
        file_url = file_url_prefix + file_url

        response = requests.head(url=file_url)
        value, params = cgi.parse_header( response.headers['Content-Disposition'] )
        # 按照规范转换文件名
        file_name = params['filename'].encode('ISO-8859-1').decode('utf8')

        self.download_file(file_url, save_folder + '/' + file_name)
        pass

    # 解析课程表，将一个学习的课程表对应的链接都获取到
    # only_list 表示只列出链接，不进行下载，默认为 0，设置为 1 时表示列出链接并进行下载
    def parse_table(self, table_start_url, only_list = 0):
        # 解析 url 中带的参数
        result = urllib.parse.urlsplit(table_start_url)
        url_paras = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(table_start_url).query))

        if( not "grade" in url_paras ):
            print( " grade 属性不存在，请明确需要获取的年级。")
            return False

        html = self.get_html(table_start_url)

        # 遍历需要下载的视频和视频标题
        soup = BeautifulSoup(html, 'html.parser')
        work_table = soup.find_all('table', attrs={'class':'content_table', 'grade' : url_paras['grade']})

        for item in work_table:

            i = 0
            j = 0
            # 表格为6行6列，国庆期间表格较为特殊，最大表格为7行7列
            table_data = [ ['' for m in range(7)] for n in range(7) ]
            # print(table_data)
            
            trs = item.find_all('tr')
            for tr in trs:
                cells = tr.find_all('th')
                if not cells:
                    cells = tr.find_all('td')
                for cell in cells:
                    table_data[i][j] = cell.get_text()
                    print(cell.get_text())
                    # 对于三年级下学期，如果有“一课一包”，则下载所有文件并跳过后续
                    if "一课一包" in cell.get_text():
                        # print(cell)
                        print(cell.a['href'])
                    # 把含有语文的内容记录下来
                    elif "语文" in cell.get_text():
                        print(table_data[0][j].strip().split("\n")[0] + "," + cell.get_text().strip().split("\n")[3] + "," + cell.a['href'])
                        pass
                        # 获取课程页面内容
                        # course_html = self.get_html(cell.a['href'])
                        # self.download_files(cell.a['href'], table_data[0][j].strip().split("\n")[0] + "-" + cell.get_text().strip().split("\n")[3])
                    j = j + 1
                i = i + 1
                j = 0

        print( "完成所有课程资源的下载！" )
        pass

    def test(self):
        course_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/weike/dcb83ca48c8d819e2cbf2279df0a9009.html?grade_id=3&subject_id=1"
        response = requests.get(course_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取课程名称
        lesson_name = soup.find('span', attrs = {'id':'album_lesson_name'})
        print(lesson_name.text)

        # 获取视频资源的链接地址
        video_url = re.search(r'videourl="(.*)"', response.text).group(1).strip()
        print("Video Url : " + video_url)

        # 获取需要下载的文件列表
        file_lists = soup.find_all('div', attrs = {'class':'recourse_item'})
        for f in file_lists:
            print("File name:" + f.get_text().strip())
            print("Download Url:" + f.a['href'])

        pass

# 保存路径规划
# teaching_resource / YYYY-MM-DD-Name / xxxx.video,ppt,docx

# 实例化
course_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/weike/ca7cbfb74525d1f3356de6fcb1731563.html?grade_id=3&subject_id=1&_d=2020/12/28"
video_url = "https://video.cache.bdschool.cn/vd/be520d8037ee8ed5a01b0ac502d3caa2.mp4?s=f164c7f3afa596cb3339e018c746fb87&c=301785&id=63701"
# file_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=908001"
file_url = "https://cache.bdschool.cn/index.php?app=interface&mod=Resource&act=download&id=872507"

# 三年级上册
# table_start_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/w.html?grade=3"

# 三年级下册
# table_start_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/prev_w.html?grade=3&_d=2021/02/23"

# 四年级下册
# table_start_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/2020_d_w.html"
table_start_url = "https://cache.bdschool.cn/public/bdschool/index/static/migu/2020_d_w.html?grade=4&_d=2022/01/15"

dog = kzkt()
dog.parse_table(table_start_url)

# dog.save_file(file_url,'./teaching_resource')
# dog.test()
# dog.parse_video(dog.get_html(url))
# dog.download_file(video_url, 'videos')
# dog.download_files(course_url, 'test')