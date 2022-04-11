# -*- coding: utf-8 -*-

import os
import sys
import atexit
import time
import threading

# Poem Spider Deamon
# 每 x 分钟从配置文件扫描需要抓取的网站
# 每 x 分钟记录当前抓取的进展

def ps_daemon():
    print("Start ps daemon")
    time.sleep(10)
    print("End ps daemon")

print("Main Process Start")
m = threading.Thread(target=ps_daemon, args=())
m.start()
time.sleep(1)