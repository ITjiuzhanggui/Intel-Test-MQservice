#!/usr/bin/env python
import os, sys
import re
import json
from pprint import pprint
import pandas as pd
from openpyxl import load_workbook

data = {
    "Default_docker": {},
    "Clear_docker": {}
}


def open_logs(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        return f.readlines()


def extract_logs(lines):
    """Test docker hub official image"""
    for i in lines[1:lines.index(
            "[mariadb] [INFO] Test clear docker image:\n")]:
        i = i.strip()
        if i.startswith("Average number of seconds"):
            average = i.split()
            data.get("Default_docker").update(
                {"Average number of seconds to run all queries": average[-2]}
            )
        if i.startswith("Minimum number of seconds"):
            minimum = i.split()
            data.get("Default_docker").update(
                {"Minimum number of seconds to run all queries": minimum[-2]}
            )
        if i.startswith("Maximum number of seconds"):
            maximum = i.split()
            data.get("Default_docker").update(
                {"Maximum number of seconds to run all queries": maximum[-2]}
            )
    """Test clear docker image"""
    for i in lines[
             lines.index("[mariadb] [INFO] Test clear docker image:\n"):]:
        i = i.strip()
        if i.startswith("Average number of seconds"):
            average = i.split()
            data.get("Clear_docker").update(
                {"Average number of seconds to run all queries": average[-2]}
            )
        if i.startswith("Minimum number of seconds"):
            minimum = i.split()
            data.get("Clear_docker").update(
                {"Minimum number of seconds to run all queries": minimum[-2]}
            )
        if i.startswith("Maximum number of seconds"):
            maximum = i.split()
            data.get("Clear_docker").update(
                {"Maximum number of seconds to run all queries": maximum[-2]}
            )
    """Test clear docker image"""


def main():
    # log_file = sys.argv[1]
    log_file = "mariadb.log"
    extract_logs(log_file)


if __name__ == '__main__':
    main()
    # pprint(data)
    df_temp = pd.DataFrame(data)
    df = df_temp.reindex(
        ['Average number of seconds to run all queries',
         'Minimum number of seconds to run all queries',
         'Maximum number of seconds to run all queries']
    )
    pprint(df)
