#!/usr/bin/env python3
import os, sys
import re
import json
from pprint import pprint
import pandas as pd
from openpyxl import load_workbook


data = {
        "Default_docker":{},
        "Clear_docker":{}
        }

def open_logs(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        return f.readlines()

def extract_logs(lines):
    """Test docker hub official image"""
    for i in lines[1:lines.index(
            "[tensorflow] [INFO] Test clear docker image:\n")]:
        if i.startswith("Total duration"):
            score = i.split()
            data.get("Default_docker").update(
                {"Total duration": score[-2]}
            )
    """Test clear docker image"""
    for i in lines[
             lines.index("[tensorflow] [INFO] Test clear docker image:\n"):]:
        if i.startswith("Total duration"):
            score = i.split()
            data.get("Clear_docker").update(
                {"Total duration": score[-2]}
            )
def main():
    log_file = sys.argv[1]
#    log_file = 'node_test.log'
    log_list = open_logs(log_file)
    extract_logs(log_list)

if __name__ == '__main__':
    main()
    #pprint(data)
    df = pd.DataFrame(data)
    pprint(df)

