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
    lines_a = lines[1:lines.index("[cassandra] [INFO] Test clear docker image:\n")].copy()
    line_nu11 = []
    line_nu12 = []

    for i in lines_a:
        if re.search(r"Op rate", i) != None:
            line_nu11.append(lines_a.index(i))

    for j in lines_a:
        if re.search(r"Latency mean", j) != None:
            line_nu12.append(lines_a.index(j))
        # pprint(line_nu11)
    wo = lines_a[int(line_nu11[0])].split()
    # pprint(wo)
    r4o = lines_a[int(line_nu11[1])].split()
    r8o = lines_a[int(line_nu11[2])].split()
    r16o = lines_a[int(line_nu11[3])].split()
    r24o = lines_a[int(line_nu11[4])].split()
    r36o = lines_a[int(line_nu11[5])].split()
    r54o = lines_a[int(line_nu11[6])].split()

    wl = lines_a[int(line_nu12[0])].split()
    r4l = lines_a[int(line_nu12[1])].split()
    r8l = lines_a[int(line_nu12[2])].split()
    r16l = lines_a[int(line_nu12[3])].split()
    r24l = lines_a[int(line_nu12[4])].split()
    r36l = lines_a[int(line_nu12[5])].split()
    r54l = lines_a[int(line_nu12[6])].split()

    data.get("Default_docker").update(
        {"cassandra-stress write test - Op rate(op/s)": wo[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress write test - Latency mean(ms)": wl[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 4 threads - Op rate(op/s)": r4o[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 4 threads - Latency mean(ms)": r4l[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 8 threads - Op rate(op/s)": r8o[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 8 threads - Latency mean(ms)": r8l[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 16 threads - Op rate(op/s)": r16o[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 16 threads - Latency mean(ms)": r16l[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 24 threads - Op rate(op/s)": r24o[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 24 threads - Latency mean(ms)": r24l[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 36 threads - Op rate(op/s)": r36o[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 36 threads - Latency mean(ms)": r36l[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 54 threads - Op rate(op/s)": r54o[3]}
    )
    data.get("Default_docker").update(
        {"cassandra-stress read test - 54 threads - Latency mean(ms)": r54l[3]}
    )

    """Test clear docker image"""
    lines_b = lines[lines.index("[cassandra] [INFO] Test clear docker image:\n"):].copy()
    line_nu21 = []
    line_nu22 = []

    for i in lines_b:
        if re.search(r"Op rate", i) != None:
            line_nu21.append(lines_b.index(i))

    for j in lines_b:
        if re.search(r"Latency mean", j) != None:
            line_nu22.append(lines_b.index(j))
    #    pprint(line_nu21)
    wo = lines_b[int(line_nu21[0])].split()
    #    pprint(wo)
    r4o = lines_b[int(line_nu21[1])].split()
    r8o = lines_b[int(line_nu21[2])].split()
    r16o = lines_b[int(line_nu21[3])].split()
    r24o = lines_b[int(line_nu21[4])].split()
    r36o = lines_b[int(line_nu21[5])].split()
    r54o = lines_b[int(line_nu21[6])].split()

    wl = lines_b[int(line_nu22[0])].split()
    r4l = lines_b[int(line_nu22[1])].split()
    r8l = lines_b[int(line_nu22[2])].split()
    r16l = lines_b[int(line_nu22[3])].split()
    r24l = lines_b[int(line_nu22[4])].split()
    r36l = lines_b[int(line_nu22[5])].split()
    r54l = lines_b[int(line_nu22[6])].split()

    data.get("Clear_docker").update(
        {"cassandra-stress write test - Op rate(op/s)": wo[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress write test - Latency mean(ms)": wl[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 4 threads - Op rate(op/s)": r4o[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 4 threads - Latency mean(ms)": r4l[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 8 threads - Op rate(op/s)": r8o[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 8 threads - Latency mean(ms)": r8l[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 16 threads - Op rate(op/s)": r16o[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 16 threads - Latency mean(ms)": r16l[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 24 threads - Op rate(op/s)": r24o[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 24 threads - Latency mean(ms)": r24l[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 36 threads - Op rate(op/s)": r36o[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 36 threads - Latency mean(ms)": r36l[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 54 threads - Op rate(op/s)": r54o[3]}
    )
    data.get("Clear_docker").update(
        {"cassandra-stress read test - 54 threads - Latency mean(ms)": r54l[3]}
    )


def main():
    # log_file = sys.argv[1]
    log_file = r'C:\Users\xinhuizx\Intel-Test-MQservice\2019-07-20-AWS\test_log\cassandra\2019-07-21-09_31_20.log'
    log_list = open_logs(log_file)
    extract_logs(log_list)
    df_temp = pd.DataFrame(data)
    df = df_temp.reindex(
        ['cassandra-stress write test - Op rate(op/s)', 'cassandra-stress write test - Latency mean(ms)',
         'cassandra-stress read test - 4 threads - Op rate(op/s)',
         'cassandra-stress read test - 4 threads - Latency mean(ms)',
         'cassandra-stress read test - 8 threads - Op rate(op/s)',
         'cassandra-stress read test - 8 threads - Latency mean(ms)',
         'cassandra-stress read test - 16 threads - Op rate(op/s)',
         'cassandra-stress read test - 16 threads - Latency mean(ms)',
         'cassandra-stress read test - 24 threads - Op rate(op/s)',
         'cassandra-stress read test - 24 threads - Latency mean(ms)',
         'cassandra-stress read test - 36 threads - Op rate(op/s)',
         'cassandra-stress read test - 36 threads - Latency mean(ms)',
         'cassandra-stress read test - 54 threads - Op rate(op/s)',
         'cassandra-stress read test - 54 threads - Latency mean(ms)'])
    pprint(df)

    with open('data_NEW.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()
    # pprint(data)
#    df_temp = pd.DataFrame(data)
#    df = df_temp.reindex(['Time taken for tests(s)', 'Time per request(ms)', 'Time per request(ms)(across all concurrent requests)', 'Requests per second(#/sec)', 'Transfer rate (Kbytes/sec) received'])
#    pprint(df)
#    basestation = "/root/lbj/results/20190610/cassandra.xlsx"
#    df.to_excel(basestation)
#    writer = pd.ExcelWriter(basestation)
#    df.to_excel(writer, sheet_name='Sheet1')
#    df.to_excel(writer, sheet_name='B')
#    writer.save()
#    writer.close()
