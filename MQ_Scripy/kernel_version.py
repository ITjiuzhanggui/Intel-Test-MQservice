#!/usr/bin/env python3
import re
from pprint import pprint

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
    with open(file_name, 'r', encoding='utf-8')as f:
        return f.readlines()


def httpd(lines):
    for i in lines[
             lines.index("[httpd] [INFO] default package version:\n"):]:

        if i.startswith("Server version:"):
            # httpd = i.split()

            httpd = re.findall("^-?[1-9]d*$", i)
            print(httpd)



def python(lines):
    lines = lines[lines.index("[python] [INFO] default package version:\n"):
                  lines.index("Reading package lists...\n")].copy()

    for i in lines:
        if i.startswith("Python"):
            python = i.split()
            data.get("default").get("python").update(
                {"python_version": python[-1]})


def main():
    file_name = r'C:\Users\xinhuizx\Intel-Test-MQservice\log\2019-08-05-Clr\test_log\httpd\2019-08-05-16_51_29.log'
    test = read_logs(file_name)

    httpd(test)
    # python(test)

    pprint(data)


if __name__ == '__main__':
    main()
