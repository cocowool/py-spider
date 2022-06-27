# -*- coding: utf-8 -*-
import os
import json
import time
import pypinyin

# Convert spider json files to markdown file

def get_human_time():
    fmt = '%Y-%m-%d %H:%M:%S'

    ts = time.time()
    ta = time.localtime(ts)
    t = time.strftime(fmt, ta)
    return t

# 将汉字转换为拼音
def word2pinyin(word):
    s = ''
    for i in pypinyin.pinyin( word, style=pypinyin.NORMAL):
        s += ''.join(i)
    
    return s

# markdown file name pattern "唐-李白-静夜思"
def save_to_markdown(json_content, markdown_file):
    md_string = ''
    hexo_date = get_human_time()
    hexo_top = '''---
title: {hexo_title}
date: {hexo_date}
tag: 
---\n'''.format(hexo_title=json_content['p_title'], hexo_date=hexo_date)

    md_string += hexo_top

    md_string += '## ' + json_content['p_title'] + '\n'
    md_string += '\n'
    md_string += '> ' + json_content['p_author'] + ' \n'
    md_string += '\n'
    md_string += json_content['p_content']

    if markdown_file is not '':
        # print(md_string)
        with open( markdown_file, 'w') as fp:
            fp.write(md_string)
        fp.close()
        print( "Saved to : " + markdown_file)



if __name__ == "__main__":
    json_files = '/Users/shiqiang/Projects/shici123/json_files/'
    markdown_files = '/Users/shiqiang/Projects/shici123/markdown_files/'
    for parent, _, file_names in os.walk(json_files):
        for file_name in file_names:
            full_json_file = os.path.join(parent, file_name)
            markdown_file = markdown_files + file_name
            with open(full_json_file, 'r') as fp:                
                # print(full_json_file)                
                json_content = json.load(fp)
                md_file_name = json_content['p_dynasty'] + '-' + json_content['p_author'] + '-' + json_content['p_title'] + '.md'
                md_file_name = word2pinyin(md_file_name)
                md_file_name = markdown_files + md_file_name

                save_to_markdown(json_content, md_file_name)
