#!/usr/bin/env python3
import re
from pprint import pprint

data = {

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


def read_log(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.readlines()


title = ["docker.io/httpd",
         "docker.io/golang",
         "docker.io/nginx",
         "docker.io/memcached",
         "docker.io/redis",
         "docker.io/php",
         "docker.io/python",
         "docker.io/node",
         "docker.io/openjdk",
         "docker.io/ruby",
         "docker.io/tensorflow",
         "docker.io/perl",
         "docker.io/postgres",
         "docker.io/mariadb",
         "docker.io/rabbitmq",
         "docker.io/flink",
         "docker.io/cassandra"]

clr_title = ["docker.io/clearlinux/httpd",
             "docker.io/clearlinux/golang",
             "docker.io/clearlinux/nginx",
             "docker.io/clearlinux/memcached",
             "docker.io/clearlinux/redis",
             "docker.io/clearlinux/php",
             "docker.io/clearlinux/python",
             "docker.io/clearlinux/node",
             "docker.io/clearlinux/openjdk",
             "docker.io/clearlinux/ruby",
             "docker.io/clearlinux/tensorflow",
             "docker.io/clearlinux/perl",
             "docker.io/clearlinux/postgres",
             "docker.io/clearlinux/mariadb",
             "docker.io/clearlinux/rabbitmq",
             "docker.io/clearlinux/flink",
             "docker.io/clearlinux/cassandra"]

for title_def in title:


for clear_title in clr_title:
    pprint(clear_title)


def def_stu(lines):
    if_n = True
    for i in lines:
        if i.startswith("docker.io/httpd"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:
        if i.startswith("docker.io/httpd"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("httpd").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("httpd").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("httpd").update(
                {"MicroService_layer": num[0]})


def clr_stu(lines):
    if_n = True
    for i in lines:
        if i.startswith("docker.io/httpd"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("docker.io/clearlinux/httpd"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("httpd").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("httpd").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("httpd").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/httpd version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("httpd").update(
                {"VERSION_ID": num[0]}
            )


def main():
    file_name = r"C:\Users\xinhuizx\Intel-Test-MQservice\2019-07-24\status_log\2019-07-24-17_40_04.log"
    test = read_log(file_name)

    def_stu(test)
    clr_stu(test)

    pprint(data)


if __name__ == '__main__':
    main()
