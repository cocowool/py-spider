# -*- coding: utf-8 -*-
import os

# Convert spider json files to markdown file

json_files = '/Users/shiqiang/Projects/shici123/json_files/'
markdown_files = '/Users/shiqiang/Projects/shici123/markdown_files/'
for parent, _, file_names in os.walk(json_files):
    for file_name in file_names:
        print(file_name)
        markdown_file = markdown_files + file_name
