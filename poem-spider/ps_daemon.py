# -*- coding: utf-8 -*-

import os
import sys
import atexit

# Poem Spider Deamon
# 每 x 分钟从配置文件扫描需要抓取的网站
# 每 x 分钟记录当前抓取的进展