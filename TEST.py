#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import os
#
# for root, dirs, files in os.walk(".", topdown=False):
#     for name in files:
#         print(os.path.join(root, name))
# for name in dirs:
#     print(os.path.join(root, name))

from pathlib import Path
import json

analysis_root_dir = "C:\\Users\\xinhuizx\\Intel-Test-MQservice\\log\2019-08-26-Azure-Ubuntu\\test_log\\postgres"
store_result = "C:\\Users\\xinhuizx\\Intel-Test-MQservice\\json"


def parse_dir(root_dir):
    path = Path(root_dir)
    print(path)
    all_json_file = list(path.glob('**/*.json'))

    parse_result = []

    for json_file in all_json_file:
        # 获取所在目录的名称
        service_name = json_file.parent.stem
        with json_file.open() as f:
            json_result = json.load(f)
        json_result["service_name"] = service_name
        parse_result.append(json_result)

    return parse_result


def write_result_in_file(write_path, write_content):
    with open(write_path, 'w') as f:
        f.writelines("service_name,action,method,url\n")
        for dict_content in write_content:
            url = dict_content['url']
            method = dict_content['method']
            action = dict_content['action']
            service_name = dict_content['service_name']
            f.writelines(service_name + "," + action + "," + method + "," + url + "\n")


def main():
    print("main begin...")
    parse_result = parse_dir(analysis_root_dir)
    print(parse_result)
    write_result_in_file(store_result, parse_result)
    print("main finished...")


if __name__ == '__main__':
    main()
