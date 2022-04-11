# -*- coding: utf-8 -*-

import os
import sys
import atexit
import time
import threading
import signal

# Poem Spider Deamon
# 每 x 分钟从配置文件扫描需要抓取的网站
# 每 x 分钟记录当前抓取的进展

def ps_daemon(pid_file = None):
    # 从父进程 Fork 子进程出来
    pid = os.fork()
    if pid:
        sys.exit(0)

    os.chdir('/')
    os.umask(0)
    os.setsid()

    sys.stdout.flush()
    sys.stderr.flush()

    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
        atexit.register(os.remove, pid_file)

    ps_spider()

def ps_spider():
    while True:
        print("Happly Little spider")
        time.sleep(5)

if __name__ == '__main__':
    help_msg = 'Usage: python3 ps_daemon.py <start|stop|restart|status>'
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)

#     print("Start ps daemon")
#     time.sleep(10)
#     print("End ps daemon")

# print("Main Process Start")
# m = threading.Thread(target=ps_daemon, args=())
# m.start()
# time.sleep(1)
ps_daemon()