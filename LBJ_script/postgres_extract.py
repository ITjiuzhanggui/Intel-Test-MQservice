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
    lines_a = lines[1:lines.index("[postgres] [INFO] Test clear docker image:\n")].copy()
    line_nu = []
    for i in lines_a:
        if re.search(r"excluding", i) != None:
            line_nu.append(lines_a.index(i))
    #   pprint(line_nu)
    bsw = lines_a[int(line_nu[0])].split()
    bsr = lines_a[int(line_nu[1])].split()
    bnw = lines_a[int(line_nu[2])].split()
    bnr = lines_a[int(line_nu[3])].split()
    bhw = lines_a[int(line_nu[4])].split()
    bhr = lines_a[int(line_nu[5])].split()
    data.get("Default_docker").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_WRITE": bsw[2]}
    )
    data.get("Default_docker").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_ONLY": bsr[2]}
    )
    data.get("Default_docker").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_WRITE": bnw[2]}
    )
    data.get("Default_docker").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_ONLY": bnr[2]}
    )
    data.get("Default_docker").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw[2]}
    )
    data.get("Default_docker").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr[2]}
    )
	
	
	
	
    """Test clear docker image"""
    lines_b = lines[lines.index("[postgres] [INFO] Test clear docker image:\n"):].copy()
    line_nu2 = []
    for i in lines_b:
        if re.search(r"excluding", i) != None:
            line_nu2.append(lines_b.index(i))
    #    pprint(line_nu2)
    bsw2 = lines_b[int(line_nu2[0])].split()
    bsr2 = lines_b[int(line_nu2[1])].split()
    bnw2 = lines_b[int(line_nu2[2])].split()
    bnr2 = lines_b[int(line_nu2[3])].split()
    bhw2 = lines_b[int(line_nu2[4])].split()
    bhr2 = lines_b[int(line_nu2[5])].split()
    data.get("Clear_docker").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_WRITE": bsw2[2]}
    )
    data.get("Clear_docker").update(
        {"BUFFER_TEST&SINGLE_THREAD&READ_ONLY": bsr2[2]}
    )
    data.get("Clear_docker").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_WRITE": bnw2[2]}
    )
    data.get("Clear_docker").update(
        {"BUFFER_TEST&NORMAL_LOAD&READ_ONLY": bnr2[2]}
    )
    data.get("Clear_docker").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw2[2]}
    )
    data.get("Clear_docker").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr2[2]}
    )


def main():
    # log_file = sys.argv[1]
    log_file = 'postgres.log'
    log_list = open_logs(log_file)
    extract_logs(log_list)
    df_temp = pd.DataFrame(data)
    pprint(df_temp)


if __name__ == '__main__':
    main()
