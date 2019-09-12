#!/usr/bin/env python3

import os, sys
import re
import json
from pprint import pprint

import pandas as pd

data = {
    "default":
        {
            "httpd": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {}, "golang": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {}, "postgres": {}, "mariadb": {},
            "rabbitmq": {}, "flink": {}, "cassandra": {}
        },

    "clear":
        {
            "httpd": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {}, "golang": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {}, "postgres": {}, "mariadb": {},
            "rabbitmq": {}, "flink": {}, "cassandra": {}
        },

    "status_def":
        {
            "httpd": {}, "golang": {}, "nginx": {}, "memcached": {}, "redis": {}, "php": {}, "python": {},
            "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {}, "postgres": {}, "mariadb": {},
            "rabbitmq": {}, "flink": {}, "cassandra": {}
        },

    "status_Clr":
        {
            "clearlinux_version": {}, "httpd": {}, "golang": {}, "nginx": {}, "memcached": {}, "redis": {},
            "php": {}, "python": {}, "node": {}, "openjdk": {}, "ruby": {}, "tensorflow": {}, "perl": {},
            "postgres": {}, "mariadb": {}, "rabbitmq": {}, "flink": {}, "cassandra": {}
        }
}


def read_logs(file_name):
    with open(file_name, 'r', encoding="utf-8")as f:
        return f.readlines()


def read_status_logs(status_log):
    with open(status_log, 'r', encoding="utf-8")as s:
        return s.readlines()


def Log_postgres(lines, loop_count):
    """analysis postgres test log"""

    lines_a = lines[
              lines.index("postgres/postgres.sh\n"):
              lines.index("[postgres] [INFO] Test clear docker image:\n")].copy()
    line_nu = []
    for i in lines_a:
        if re.search(r"excluding", i) != None:
            line_nu.append(lines_a.index(i))
    # pprint(line_nu)
    bsw = lines_a[int(line_nu[0])].split()
    bsr = lines_a[int(line_nu[1])].split()
    bnw = lines_a[int(line_nu[2])].split()
    bnr = lines_a[int(line_nu[3])].split()
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_WRITE": bsw[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_ONLY": bsr[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_WRITE": bnw[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_ONLY": bnr[2]}
    )

    """clearlinux openjdk test log analysis"""

    lines_b = lines[
              lines.index("[postgres] [INFO] Test clear docker image:\n"):
              lines.index("Clr-Node-Server\n")].copy()
    line_nu2 = []
    for i in lines_b:
        if re.search(r"excluding", i) != None:
            line_nu2.append(lines_b.index(i))
        # pprint(line_nu2)
    bsw2 = lines_b[int(line_nu2[0])].split()
    bsr2 = lines_b[int(line_nu2[1])].split()
    bnw2 = lines_b[int(line_nu2[2])].split()
    bnr2 = lines_b[int(line_nu2[3])].split()
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_WRITE": bsw2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_ONLY": bsr2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_WRITE": bnw2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_ONLY": bnr2[2]}
    )


def main():
    loop_count = 0
    file_name = r"C:\Users\xinhuizx\Intel-Test-MQservice\log\2019-08-26-Azure-Ubuntu\test_log\postgres"
    xlsx = r"C:\Users\xinhuizx\Intel-Test-MQservice\Xlsx\111.xlsx"
    # test = read_logs(file_name)
    writer = pd.ExcelWriter(xlsx)
    # status_log = r""
    # status = read_status_logs()
    for root, _, files, in os.walk(file_name):
        for file_name in files:
            full_file_name = os.path.join(root, file_name)
            # print(full_file_name)
            test = read_logs(full_file_name)
            # print(root, files)

            # Log_openjdk(test)
            Log_postgres(full_file_name, loop_count)
            # Log_ruby(test)
            # Clr_Log_ruby(test)
            loop_count += 1

    os.write.save()


def write_result_in_file(write_path, write_content):
    with open(write_path, 'w')as f:
        f.writelines()


if __name__ == '__main__':
    main()
    pprint(data)
