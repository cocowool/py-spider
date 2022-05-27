# -*- coding: utf-8 -*-

from doctest import FAIL_FAST
import os
import sys
import atexit
import time
import threading
import signal

# Poem Spider Deamon
# 每 x 分钟从配置文件扫描需要抓取的网站
# 每 x 分钟记录当前抓取的进展

class DeamonDecorator:
    pass

class PoemSpiderDeamon:
    # 初始化
    def __init__(self, pid_path, stdin = os.devnull, stdout = os.devnull, stderr = os.devnull, home_dir = '.', umask = '022', verbose = 1):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pid_path = pid_path
        self.home_dir = home_dir
        self.umask = umask
        self.verbose = verbose
        self.daemon_alive = True

        super().__init__()

    def ps_daemon(self):
        #@TODO 本处忽略了错误处理
        pid = os.fork()
        if pid:
            sys.exit(0)

        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        pid = os.fork()
        if pid:
            sys.exit(0)

        sys.stdout.flush()
        sys.stderr.flush()

        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        if self.stderr:
            se = open(self.stderr, 'a+', 0)
        else:
            se = so

        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        def sig_handler(signum ,frame):
            self.daemon_alive = False

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

ps_daemon()

# if __name__ == '__main__':
#     help_msg = 'Usage: python3 ps_daemon.py <start|stop|restart|status>'
#     if len(sys.argv) != 2:
#         print(help_msg)
#         sys.exit(1)

#     psd_name = 'poem_spider_daemon'
#     pid_file = '/Users/shiqiang/Projects/py-spider/poem-spider/psd.pid'
#     log_file = '/Users/shiqiang/Projects/py-spider/poem-spider/psd.log'
#     err_file = '/Users/shiqiang/Projects/py-spider/poem-spider/psd-error.log'

#     psd = PoemSpiderDeamon(psd_name, pid_file, stderr=err_file, verbose=1)

#     if sys.argv[1] == 'start':
#         psd.start(log_file)
#     elif sys.argv[1] == 'stop':
#         psd.stop()
#     elif sys.argv[1] == 'restart':
#         psd.restart(log_file)
#     elif sys.argv[1] == 'status':
#         alive = psd.is_running()
#         if alive:
#             print("Poem Daemon [%s] is running ......" % (psd.get_pid()) )
#         else:
#             print("Poem Daemon stopped")
#     else:
#         print("Invalid parameter")
#         print(help_msg)