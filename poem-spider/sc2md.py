# -*- coding: utf-8 -*-
import os
import json

# Convert spider json files to markdown file

# markdown file name pattern "唐-李白-静夜思"
def save_to_markdown(json_content, markdown_file):
    pass


if __name__ == "__main__":
    json_files = '/Users/shiqiang/Projects/shici123/json_files/'
    markdown_files = '/Users/shiqiang/Projects/shici123/markdown_files/'
    for parent, _, file_names in os.walk(json_files):
        for file_name in file_names:
            full_json_file = os.path.join(parent, file_name)
            markdown_file = markdown_files + file_name
            with open(full_json_file, 'r') as fp:
                json_content = json.load(fp)
                print(json_content)