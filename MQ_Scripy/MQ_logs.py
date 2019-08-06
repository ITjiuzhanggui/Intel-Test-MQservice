#!/usr/bin/env python3

import os, sys
import re
import json
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

# !/usr/bin/env python3
# import time
# import os
#
# cmd = "make memcached"
# logs_path = "/home/log"
# for i in range(5):
#     os.system("{} > {}/{}.log 2>&1 ".format(cmd, logs_path,\
#         time.strftime("%Y-%m-%d-%H:%M:%S", \
#         time.localtime()).replace(' ',':').replace(':', ':')))

"""default test_long"""


def read_logs(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        return f.readlines()


def read_status_logs(status_log):
    with open(status_log, "r", encoding="utf-8") as s:
        return s.readlines()


def default_from_httpd(lines):
    """httpd unit tests analysis"""
    for i in lines[lines.index("httpd/httpd.sh\n"):lines.index("httpd-server\n")]:
        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("httpd").update(
                {"Transfer rate": num[0]}
            )


def default_from_nginx(lines):
    """nginx unit tests analysis"""

    for i in lines[
             lines.index("[nginx] [INFO] Test docker hub official image first:\n"):
             lines.index("[nginx] [INFO] Test clear docker image:\n")]:

        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("nginx").update(
                {"Transfer rate": num[0]}
            )


# def default_from_memcached(lines):
#     '''memcached unit tests analysis'''
#
#     for i in lines[lines.index("memcached/memcached.sh\n"):lines.index("memcached-server\n")]:
#         if i.startswith("Sets"):
#             num = re.findall("---|\d+\.?\d*", i)
#             num[-1] += " KB/sec"
#             data.get("default").get("memcached").update(
#                 {"Sets": num[-2:]})
#
#         if i.startswith("Gets"):
#             num = re.findall("---|\d+\.?\d*", i)
#             num[-1] += " KB/sec"
#             data.get("default").get("memcached").update(
#                 {"Gets": num[-2:]})
#
#         if i.startswith("Totals"):
#             num = re.findall("---|\d+\.?\d*", i)
#             num[-1] += " KB/sec"
#             data.get("default").get("memcached").update(
#                 {"Totals": num[-2:]})


def default_from_memcached(lines):
    '''memcached unit tests analysis'''

    for i in lines[
             lines.index("memcached/memcached.sh\n"):
             lines.index("Default-Memcached-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)
            data.get("default").get("memcached").update(
                {"Sets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)
            data.get("default").get("memcached").update(
                {"Gets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)
            data.get("default").get("memcached").update(
                {"Totals": ["Latency:" + num[-2], num[-1] + " KB/sec"]})


def default_from_redis(lines):
    """redis unit tests analysis"""

    influs_defaut = []
    for i in lines[
             lines.index("redis/redis.sh\n"):
             lines.index("Default-Redis-Server\n")]:
        influs_defaut.append(i)

    for i in influs_defaut[
             influs_defaut.index("====== PING_INLINE ======\n"):
             influs_defaut.index("====== PING_BULK ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"PING_INLINE": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== PING_BULK ======\n"):
             influs_defaut.index("====== SET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"PING_BULK": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SET ======\n"):
             influs_defaut.index("====== GET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== GET ======\n"):
             influs_defaut.index("====== INCR ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"GET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== INCR ======\n"):
             influs_defaut.index("====== LPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"INCR": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH ======\n"):
             influs_defaut.index("====== RPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPUSH ======\n"):
             influs_defaut.index("====== LPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"RPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPOP ======\n"):
             influs_defaut.index("====== RPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPOP ======\n"):
             influs_defaut.index("====== SADD ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"RPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SADD ======\n"):
             influs_defaut.index("====== HSET ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SADD": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== HSET ======\n"):
             influs_defaut.index("====== SPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"HSET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SPOP ======\n"):
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"SPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):
             influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LPUSH (needed to benchmark LRANGE)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):
             influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_100 (first 100 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):
             influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_300 (first 300 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_500 (first 450 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):
             influs_defaut.index("====== MSET (10 keys) ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"LRANGE_600 (first 600 elements)": num[0]}
            )

    influs_defaut.append("Default-Redis-Server\n")
    for i in influs_defaut[
             influs_defaut.index("====== MSET (10 keys) ======\n"):
             influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("redis").update(
                {"MSET (10 keys)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n"):
             influs_defaut.index("Default-Redis-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("default").get("redis").update(
                {"Sets-Latency:": num[-2]})
            data.get("default").get("redis").update(
                {"Sets-KB/sec": num[-1]}
            )

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("default").get("redis").update(
                {"Gets-Latency:": num[-2]})
            data.get("default").get("redis").update(
                {"Gets-KB/sec": num[-1]}
            )

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("default").get("redis").update(
                {"Totals-Latency:": num[-2]})
            data.get("default").get("redis").update(
                {"Totals-KB/sec": num[-1]}
            )


def default_from_php(lines):
    """php unit tests analysis"""

    for i in lines[lines.index("php/php.sh\n"):lines.index("[php] [INFO] Test clear docker image:\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("php").update(
                {"phpbench": num[0]}
            )


def default_from_python(lines):
    """python unit tests analysis"""

    # for i in lines[lines.index("python/python.sh\n"):lines.index("Default-Python-Server\n")]:
    lines = lines[lines.index("python/python.sh\n"):
                  lines.index("[python] [INFO] Test clear docker image:\n")].copy()

    for i in lines:
        if i.startswith("Totals"):
            num = re.findall("\d+\.?\d*", i)
            num[0] = {"minimum": num[0]}
            num[1] = {"average": num[1]}
            data.get("default").get("python").update(
                {"Totals": num[-2:]}
            )


def default_from_golang(lines):
    """golang unit tests analysis"""

    for i in lines[
             lines.index("golang/golang.sh\n"):
             lines.index("Default-Golang-Server\n")]:

        if i.startswith("BenchmarkBuild"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkBuild": num[0][:-6]}
            )

        if i.startswith("BenchmarkGarbage"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkGarbage": num[0][:-6]}
            )

        if i.startswith("BenchmarkHTTP"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkHTTP": num[0][:-6]}
            )

        if i.startswith("BenchmarkJSON"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("default").get("golang").update(
                {"BenchmarkJSON": num[0][:-6]}
            )


def default_from_nodejs(lines):
    """nodejs unit tests analysis"""
    for i in lines[
             lines.index("node/node.sh\n"):
             lines.index("Default-Node-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("node").update(
                {"benchmark-node-octane": num[-1]}
            )


def default_from_openjdk(lines):
    """openjdk unit tests analysis"""
    for i in lines[
             lines.index("[openjdk] [INFO] Test docker hub official image first:\n"):
             lines.index("[openjdk] [INFO] Test clear docker image:\n")]:

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("default").get("openjdk").update(
                {"MyBenchmark.testMethod.Score": num[-2]}
            )

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d+", i)
            data.get("default").get("openjdk").update(
                {"MyBenchmark.testMethod.Error": num[-1]}
            )


def default_from_postgres(lines):
    """postgres unit tests analysis"""
    lines_a = lines[
              1:lines.index("[postgres] [INFO] Test clear docker image:\n")].copy()
    line_nu = []
    for i in lines_a:
        if re.search(r"excluding", i) != None:
            line_nu.append(lines_a.index(i))
    pprint(line_nu)
    bsw = lines_a[int(line_nu[0])].split()
    bsr = lines_a[int(line_nu[1])].split()
    bnw = lines_a[int(line_nu[2])].split()
    bnr = lines_a[int(line_nu[3])].split()
    bhw = lines_a[int(line_nu[4])].split()
    bhr = lines_a[int(line_nu[5])].split()
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
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw[2]}
    )
    data.get("default").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr[2]}
    )


def default_from_tensorflow(lines):
    """tensorflow unit tests analysis"""
    for i in lines[
             lines.index("[tensorflow] [INFO] Test docker hub official image first:\n"):
             lines.index("[tensorflow] [INFO] Test clear docker image:\n")]:

        if i.startswith("Total duration"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("tensorflow").update(
                {"Total duration": num[0]})


def default_from_mariadb(lines):
    """mariadb unit tests analysis"""

    for i in lines[
             lines.index("[mariadb] [INFO] Test docker hub official image first:\n"):
             lines.index("[mariadb] [INFO] Test clear docker image:\n")]:

        i = i.strip()
        if i.startswith("Average number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("mariadb").update(
                {"Average number of seconds to run all queries": num[0]}
            )

        if i.startswith("Minimum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("mariadb").update(
                {"Minimum number of seconds to run all queries": num[0]}
            )

        if i.startswith("Maximum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("mariadb").update(
                {"Maximum number of seconds to run all queries": num[0]}
            )


def default_from_ruby(lines):
    """ruby unit tests analysis"""
    newlines = lines[
               lines.index("[ruby] [INFO] Test docker hub official image first:\n"):
               lines.index("[ruby] [INFO] Test clear docker image:\n")].copy()

    line_str_key = "Calculating"
    line_dict = {}
    ret_lines = []
    for i in range(0, len(newlines)):
        line_dict[i] = newlines[i].split("\n")[0]

    for lineno, line_str in line_dict.items():
        if line_str.startswith(line_str_key):
            # print(lineno, ":", line_str)
            tmp_line_no = lineno + 1
            while True:
                if newlines[tmp_line_no] != "\n":
                    if "so_k_nucleotidepreparing" in newlines[tmp_line_no]:
                        ret_lines.append("so_k_nucleotidepreparing " + newlines[tmp_line_no + 1])
                    if "so_reverse_complementpreparing" in newlines[tmp_line_no]:
                        ret_lines.append("so_reverse_complementpreparing " + newlines[tmp_line_no + 1])
                    ret_lines.append(newlines[tmp_line_no])
                else:
                    break
                tmp_line_no += 1

    ret_line_list = []
    for line in ret_lines:
        # print(line)
        line_split = line.split()
        key_str = line_split[0]
        value = line_split[1]
        if "Time" in line:
            time_line_split = line.split("s -")[0].split(")")
            # print(time_line_split)
            time_key = time_line_split[0].strip() + ")"
            time_value = time_line_split[-1].strip()
            # print(time_value)
            ret_line_list.append({time_key: time_value})
        elif not value.startswith("/"):
            # print(value)
            try:
                key_str = float(str(key_str))
            except Exception:
                pass
            if not isinstance(key_str, float):
                ret_line_list.append({key_str: value})
    # pprint(ret_line_list)
    # print(len(ret_line_list))
    for tmp_dict in ret_line_list:
        data.get("default").get("ruby").update(tmp_dict)

    # influs_list = ["app_answer", "app_aobench", "app_erb", "app_factorial",
    #                "app_fib", "app_lc_fizzbuzz", "app_mandelbrot", "app_pentomino",
    #                "app_raise", "app_strconcat", "app_tak", "app_tarai", "app_uri",
    #                "array_sample_100k_10", "array_sample_100k_11", "array_sample_100k__100",
    #                "array_sample_100k__1k", "array_sample_100k__6k", "array_sample_100k___10k",
    #                "array_sample_100k___50k", "array_shift", "array_small_and", "array_small_diff",
    #                "array_small_or", "array_sort_block", "array_sort_float", "array_values_at_int",
    #                "array_values_at_range", "bighash", "complex_float_add", "complex_float_div",
    #                "complex_float_mul", "complex_float_new", "complex_float_power", "complex_float_sub",
    #                "dir_empty_p", "enum_lazy_grep_v_100", "enum_lazy_grep_v_20", "enum_lazy_grep_v_50",
    #                "enum_lazy_uniq_100", "enum_lazy_uniq_20", "enum_lazy_uniq_50", "erb_render",
    #                "fiber_chain", "file_chmod", "file_rename", "hash_aref_dsym", "hash_aref_dsym_long",
    #                "hash_aref_fix", "hash_aref_flo", "hash_aref_miss", "hash_aref_str", "hash_aref_sym",
    #                "hash_aref_sym_long", "hash_flatten", "hash_ident_flo", "hash_ident_num", "hash_ident_obj",
    #                "hash_ident_str", "hash_ident_sym", "hash_keys", "hash_literal_small2", "hash_literal_small4",
    #                "hash_literal_small8", "hash_long", "hash_shift", "hash_shift_u16", "hash_shift_u24",
    #                "hash_shift_u32", "hash_small2", "hash_small4", "hash_small8", "hash_to_proc",
    #                "hash_values", "int_quo", "io_copy_stream_write", "io_copy_stream_write_socket",
    #                "io_file_create", "io_file_read", "io_file_write", "io_nonblock_noex", "io_nonblock_noex2",
    #                "io_pipe_rw", "io_select", "io_select2", "io_select3", "loop_for", "loop_generator",
    #                "loop_times", "loop_whileloop", "loop_whileloop2", "marshal_dump_flo", "marshal_dump_load_geniv",
    #                "marshal_dump_load_time",
    #                "Calculating-(1..1_000_000).last(100)",
    #                "Calculating-(1..1_000_000).last(1000)",
    #                "Calculating-(1..1_000_000).last(10000)",
    #                "capitalize-1",
    #                "capitalize-10",
    #                "capitalize-100",
    #                "capitalize-1000",
    #                "downcase-1",
    #                "downcase-10",
    #                "downcase-100",
    #                "downcase-1000",
    #                "require", "require_thread", "securerandom", "so_ackermann",
    #                "so_array", "so_binary_trees", "so_concatenate", "so_count_words", "so_exception", "so_fannkuch",
    #                "so_fasta", "so_k_nucleotidepreparing", "so_lists", "so_mandelbrot", "so_matrix",
    #                "so_meteor_contest",
    #                "so_nbody", "so_nested_loop", "so_nsieve", "so_nsieve_bits", "so_object", "so_partial_sums",
    #                "so_pidigits", "so_random", "so_reverse_complementpreparing", "so_sieve", "so_spectralnorm",
    #                "string_index", "string_scan_re",
    #                "string_scan_str",
    #                "to_chars-1",
    #                "to_chars-10",
    #                "to_chars-100",
    #                "to_chars-1000",
    #                "swapcase-1",
    #                "swapcase-10",
    #                "swapcase-100",
    #                "swapcase-1000",
    #                "upcase-1",
    #                "upcase-10",
    #                "upcase-100",
    #                "upcase-1000",
    #                """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""",
    #                """Time.strptime("1", "%s")""",
    #                """Time.strptime("0 +0100", "%s %z")""",
    #                """Time.strptime("0 UTC", "%s %z")""",
    #                """Time.strptime("1.5", "%s.%N")""",
    #                """Time.strptime("1.000000000001", "%s.%N")""",
    #                """Time.strptime("20010203 -0200", "%Y%m%d %z")""",
    #                """Time.strptime("20010203 UTC", "%Y%m%d %z")""",
    #                """Time.strptime("2018-365", "%Y-%j")""",
    #                """Time.strptime("2018-091", "%Y-%j")""",
    #                "time_subsec", "vm1_attr_ivar",
    #                "vm1_attr_ivar_set",
    #                "vm1_block", "vm1_blockparam", "vm1_blockparam_call", "vm1_blockparam_pass",
    #                "vm1_blockparam_yield",
    #                "vm1_const", "vm1_ensure", "vm1_float_simple", "vm1_gc_short_lived",
    #                "vm1_gc_short_with_complex_long",
    #                "vm1_gc_short_with_long", "vm1_gc_short_with_symbol", "vm1_gc_wb_ary", "vm1_gc_wb_ary_promoted",
    #                "vm1_gc_wb_obj", "vm1_gc_wb_obj_promoted", "vm1_ivar", "vm1_ivar_set", "vm1_length",
    #                "vm1_lvar_init",
    #                "vm1_lvar_set", "vm1_neq", "vm1_not", "vm1_rescue", "vm1_simplereturn", "vm1_swap", "vm1_yield",
    #                "vm2_array", "vm2_bigarray", "vm2_bighash", "vm2_case", "vm2_case_lit", "vm2_defined_method",
    #                "vm2_dstr", "vm2_eval", "vm2_fiber_switch", "vm2_freezestring", "vm2_method",
    #                "vm2_method_missing",
    #                "vm2_method_with_block", "vm2_module_ann_const_set", "vm2_module_const_set", "vm2_mutex",
    #                "vm2_newlambda",
    #                "vm2_poly_method", "vm2_poly_method_ov", "vm2_poly_singleton", "vm2_proc", "vm2_raise1",
    #                "vm2_raise2",
    #                "vm2_regexp", "vm2_send", "vm2_string_literal", "vm2_struct_big_aref_hi",
    #                "vm2_struct_big_aref_lo",
    #                "vm2_struct_big_aset", "vm2_struct_big_href_hi", "vm2_struct_big_href_lo", "vm2_struct_big_hset",
    #                "vm2_struct_small_aref", "vm2_struct_small_aset", "vm2_struct_small_href",
    #                "vm2_struct_small_hset",
    #                "vm2_super", "vm2_unif1", "vm2_zsuper", "vm3_backtrace", "vm3_clearmethodcache", "vm3_gc",
    #                "vm3_gc_old_full",
    #                "vm3_gc_old_immediate", "vm3_gc_old_lazy", "vm_symbol_block_pass", "vm_thread_alive_check1",
    #                "vm_thread_close",
    #                "vm_thread_condvar1", "vm_thread_condvar2", "vm_thread_create_join", "vm_thread_mutex1",
    #                "vm_thread_mutex2",
    #                "vm_thread_mutex3", "vm_thread_pass", "vm_thread_pass_flood", "vm_thread_pipe",
    #                "vm_thread_queue",
    #                "vm_thread_sized_queue", "vm_thread_sized_queue2", "vm_thread_sized_queue3",
    #                "vm_thread_sized_queue4"
    #                ]
    #
    # data_ruby = {}
    # for i in lines[
    #          # lines.index("[ruby] [INFO] Test clear docker image:\n"):
    #          # lines.index("Clr-Ruby-Server\n")]:
    #          lines.index("[ruby] [INFO] Test docker hub official image first:\n"):
    #          lines.index("Default-Ruby-Server\n")]:
    #
    #     for startwith_item in influs_list:
    #         # if i.startswith(startwith_item) or i.startswith("\t") and startwith_item in i:
    #         if i.endswith("s/i)\n") and startwith_item in i:
    #             num = re.findall("\d+\.?\d* s|ERROR", i)
    #             data_ruby.update({startwith_item: num[-1][:-1]})
    #
    #     if "so_reverse_complementpreparing" in i:
    #         start = lines.index(i)
    #         so_reverse_complementpreparing = lines[start + 1]
    #         num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
    #         data_ruby.update({"so_reverse_complementpreparing": num[-1][:-1]})
    #
    #     if "so_k_nucleotidepreparing" in i:
    #         start = lines.index(i)
    #         so_reverse_complementpreparing = lines[start + 1]
    #         num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
    #         data_ruby.update({"so_k_nucleotidepreparing": num[-1][:-1]})
    #
    # lines = lines[
    #         lines.index("[ruby] [INFO] Test docker hub official image first:\n"):
    #         lines.index("Default-Ruby-Server\n")]
    #
    # for item in lines:
    #     if item.startswith("Warming up --------------------------------------\n"):
    #         up = lines.index(item)
    #
    # for item in lines[up:]:
    #     if item.startswith("Comparison:\n"):
    #         down = lines[up:].index(item) + up
    #
    # for i in lines[up:down]:
    #
    #     if "(1..1_000_000).last(100)" in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"(1..1_000_000).last(100)": num[-4]})
    #
    #     if "(1..1_000_000).last(1000)" in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"(1..1_000_000).last(1000)": num[-4]})
    #
    #     if "(1..1_000_000).last(10000)" in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"(1..1_000_000).last(10000)": num[-4]})
    #
    # for i in lines[down:]:
    #
    #     if i.startswith("Warming up --------------------------------------\n"):
    #         capit_start = lines[down:].index(i) + down
    #
    # for i in lines[capit_start:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         calc_start = lines[capit_start:].index(i) + capit_start
    #
    # for i in lines[calc_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         calc_end = lines[calc_start:].index(i) + calc_start
    #
    # for i in lines[calc_start:calc_end]:
    #
    #     if "capitalize-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-1": num[1]})
    #
    #     if "capitalize-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-10": num[1]})
    #
    #     if "capitalize-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-100": num[1]})
    #
    #     if "capitalize-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-1000": num[1]})
    #
    # for i in lines[calc_end:]:
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         downcase_start = lines[calc_end:].index(i) + calc_end
    #
    # for i in lines[downcase_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         downcase_end = lines[downcase_start:].index(i) + downcase_start
    #
    # for i in lines[downcase_start:downcase_end]:
    #
    #     if "downcase-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-1": num[1]})
    #
    #     if "downcase-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-10": num[1]})
    #
    #     if "downcase-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-100": num[1]})
    #
    #     if "downcase-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-1000": num[1]})
    #
    # for i in lines[downcase_end:]:
    #     if i.startswith("Warming up --------------------------------------\n"):
    #         to_chars = lines[downcase_end:].index(i) + downcase_end
    #
    # for i in lines[to_chars:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         to_chars_start = lines[to_chars:].index(i) + to_chars
    #
    # for i in lines[to_chars_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         to_chars_end = lines[to_chars_start:].index(i) + to_chars_start
    #
    # for i in lines[to_chars_start:to_chars_end]:
    #
    #     if "to_chars-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-1": num[1]})
    #
    #     if "to_chars-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-10": num[1]})
    #
    #     if "to_chars-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-100": num[1]})
    #
    #     if "to_chars-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-1000": num[1]})
    #
    # for i in lines[to_chars_end:]:
    #
    #     if i.startswith("Warming up --------------------------------------\n"):
    #         swapcase = lines[to_chars_end:].index(i) + to_chars_end
    #
    # for i in lines[swapcase:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         swapcase_start = lines[swapcase:].index(i) + swapcase
    #
    # for i in lines[swapcase_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         swapcase_end = lines[swapcase_start:].index(i) + swapcase_start
    #
    # for i in lines[swapcase_start:swapcase_end]:
    #
    #     if "swapcase-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-1": num[1]})
    #
    #     if "swapcase-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-10": num[1]})
    #
    #     if "swapcase-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-100": num[1]})
    #
    #     if "swapcase-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-1000": num[1]})
    #
    # for i in lines[swapcase_end:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         upcase_start = lines[swapcase_end:].index(i) + swapcase_end
    #
    # for i in lines[upcase_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         upcase_end = lines[upcase_start:].index(i) + upcase_start
    #
    # for i in lines[upcase_start:upcase_end]:
    #
    #     if "upcase-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-1": num[1]})
    #
    #     if "upcase-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-10": num[1]})
    #
    #     if "upcase-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-100": num[1]})
    #
    #     if "upcase-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-1000": num[1]})
    #
    # for i in lines[upcase_end:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         time_start = lines[upcase_end:].index(i) + upcase_end
    #
    # for i in lines[time_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         time_end = lines[time_start:].index(i) + time_start
    #
    # for i in lines[time_start:time_end]:
    #
    #     if """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""": num[-4]})
    #
    #     if """Time.strptime("1", "%s")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("1", "%s")""": num[-4]})
    #
    #     if """Time.strptime("0 +0100", "%s %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("0 +0100", "%s %z")""": num[-4]})
    #
    #     if """Time.strptime("0 UTC", "%s %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("0 UTC", "%s %z")""": num[-4]})
    #
    #     if """Time.strptime("1.5", "%s.%N")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("1.5", "%s.%N")""": num[-4]})
    #
    #     if """Time.strptime("1.000000000001", "%s.%N")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("1.000000000001", "%s.%N")""": num[-4]})
    #
    #     if """Time.strptime("20010203 -0200", "%Y%m%d %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("20010203 -0200", "%Y%m%d %z")""": num[-4]})
    #
    #     if """Time.strptime("20010203 UTC", "%Y%m%d %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("20010203 UTC", "%Y%m%d %z")""": num[-4]})
    #
    #     if """Time.strptime("2018-365", "%Y-%j")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("2018-365", "%Y-%j")""": num[-4]})
    #
    #     if """Time.strptime("2018-091", "%Y-%j")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("2018-091", "%Y-%j")""": num[-4]})
    #
    # data.get("default").get("ruby").update(data_ruby)


def default_from_flink(lines):
    """flink unit tests analysis"""

    for i in lines[
             lines.index("[flink] [INFO] Test docker hub official image first:\n"):
             lines.index("Default-Flink-Server\n")]:

        if i.startswith("KeyByBenchmarks.arrayKeyBy"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"KeyByBenchmarks.arrayKeyBy": num[-2]})

        if i.startswith("KeyByBenchmarks.tupleKeyBy"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"KeyByBenchmarks.tupleKeyBy": num[-2]})

        if i.startswith("MemoryStateBackendBenchmark.stateBackends") and "MEMORY" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"MemoryStateBackendBenchmark.stateBackends-MEMORY": num[-2]})

        if i.startswith("MemoryStateBackendBenchmark.stateBackends") and " FS " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"MemoryStateBackendBenchmark.stateBackends-FS": num[-2]})

        if i.startswith("MemoryStateBackendBenchmark.stateBackends") and "_ASYNC " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"MemoryStateBackendBenchmark.stateBackends-FS_ASYNC": num[-2]})

        if i.startswith("RocksStateBackendBenchmark.stateBackends") and " ROCKS " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"RocksStateBackendBenchmark.stateBackends-ROCKS": num[-2]})

        if i.startswith("RocksStateBackendBenchmark.stateBackends") and "_INC " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"RocksStateBackendBenchmark.stateBackends-ROCKS_INC": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerAvro"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerAvro": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerKryo"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerKryo": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerPojo"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerPojo": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerRow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerRow": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerTuple"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerTuple": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1,100ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1,100ms": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "100,1ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-100,1ms": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1000,1ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,1ms": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1000,100ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,100ms": num[-2]})

        if i.startswith("SumLongsBenchmark.benchmarkCount"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"SumLongsBenchmark.benchmarkCount": num[-2]})

        if i.startswith("WindowBenchmarks.globalWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"WindowBenchmarks.globalWindow": num[-2]})

        if i.startswith("WindowBenchmarks.sessionWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"WindowBenchmarks.sessionWindow": num[-2]})

        if i.startswith("WindowBenchmarks.slidingWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"WindowBenchmarks.slidingWindow": num[-2]})

        if i.startswith("WindowBenchmarks.tumblingWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"WindowBenchmarks.tumblingWindow": num[-2]})

        if i.startswith("StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1"):
            num = re.findall("\d+\.?\d*", i)
            data.get("default").get("flink").update(
                {"StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1": num[-2]})


"""clearlinux test_log"""


def clr_from_httpd(lines):
    """clearlinux unit tests analysis"""
    for i in lines[
             lines.index("[httpd] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Httpd-Server\n")]:

        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("httpd").update(
                {"Transfer rate": num[0]}
            )


def clr_from_nginx(lines):
    """clearlinux unit test analysis"""

    for i in lines[
             lines.index("[nginx] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Nginx-Server\n")]:

        if i.startswith("Time taken for tests"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Time taken for tests": num[0]}
            )

        if i.endswith("[ms] (mean)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Time per request": num[0]}
            )

        if i.endswith("(mean, across all concurrent requests)\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Time per request(all)": num[0]}
            )

        if i.startswith("Requests per second"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Requests per second": num[0]}
            )

        if i.startswith("Transfer rate"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("nginx").update(
                {"Transfer rate": num[0]}
            )


def clr_from_memcached(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[memcached] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Memcached-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("clear").get("memcached").update(
                {"Sets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)
            # num[-1] += " KB/sec"
            data.get("clear").get("memcached").update(
                {"Gets": ["Latency:" + num[-2], num[-1] + " KB/sec"]})

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)
            # num[-1] += " KB/sec"
            data.get("clear").get("memcached").update(
                {"Totals": ["Latency:" + num[-2], num[-1] + " KB/sec"]})


def clr_from_redis(lines):
    """clearlinux unit tests analysis"""

    influs_defaut = []
    for i in lines[
             lines.index("[redis] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Redis-Server\n")]:
        influs_defaut.append(i)

    for i in influs_defaut[
             influs_defaut.index("====== PING_INLINE ======\n"):
             influs_defaut.index("====== PING_BULK ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"PING_INLINE": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== PING_BULK ======\n"):
             influs_defaut.index("====== SET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"PING_BULK": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SET ======\n"):
             influs_defaut.index("====== GET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== GET ======\n"):
             influs_defaut.index("====== INCR ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"GET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== INCR ======\n"):
             influs_defaut.index("====== LPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"INCR": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH ======\n"):
             influs_defaut.index("====== RPUSH ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPUSH ======\n"):
             influs_defaut.index("====== LPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"RPUSH": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPOP ======\n"):
             influs_defaut.index("====== RPOP ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== RPOP ======\n"):
             influs_defaut.index("====== SADD ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"RPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SADD ======\n"):
             influs_defaut.index("====== HSET ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SADD": num[0]}
            )

    for i in influs_defaut[influs_defaut.index("====== HSET ======\n"):influs_defaut.index("====== SPOP ======\n")]:
        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"HSET": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== SPOP ======\n"):
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"SPOP": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LPUSH (needed to benchmark LRANGE) ======\n"):
             influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LPUSH (needed to benchmark LRANGE)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_100 (first 100 elements) ======\n"):
             influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_100 (first 100 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_300 (first 300 elements) ======\n"):
             influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_300 (first 300 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_500 (first 450 elements) ======\n"):
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_500 (first 450 elements)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("====== LRANGE_600 (first 600 elements) ======\n"):
             influs_defaut.index("====== MSET (10 keys) ======\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"LRANGE_600 (first 600 elements)": num[0]}
            )

    influs_defaut.append("Clr-Redis-Server\n")
    for i in influs_defaut[
             influs_defaut.index("====== MSET (10 keys) ======\n"):
             influs_defaut.index("[redis] [INFO] memtier_benchmark test:\n")]:

        if i.endswith("requests per second\n"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("redis").update(
                {"MSET (10 keys)": num[0]}
            )

    for i in influs_defaut[
             influs_defaut.index("[redis] [INFO] Test clear docker image:\n"):
             influs_defaut.index("Clr-Redis-Server\n")]:

        if i.startswith("Sets"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("clear").get("redis").update(
                {"Sets-Latency:": num[-2]})
            data.get("clear").get("redis").update(
                {"Sets-KB/sec": num[-1]}
            )

        if i.startswith("Gets"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("clear").get("redis").update(
                {"Gets-Latency:": num[-2]})
            data.get("clear").get("redis").update(
                {"Gets-KB/sec": num[-1]}
            )

        if i.startswith("Totals"):
            num = re.findall("---|\d+\.?\d*", i)

            data.get("clear").get("redis").update(
                {"Totals-Latency:": num[-2]})
            data.get("clear").get("redis").update(
                {"Totals-KB/sec": num[-1]}
            )


def clr_from_php(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[php] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Php-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("php").update(
                {"Score": num[0]}
            )


def clr_from_python(lines):
    """clearlinux unit tests analysis"""
    lines = lines[lines.index("[python] [INFO] Test clear docker image:\n"):].copy()
    # for i in lines[
    #          lines.index("[python] [INFO] Test clear docker image:\n"):
    #          lines.index("Clr-Python-Server\n")]:
    for i in lines:
        if i.startswith("Totals"):
            num = re.findall("\d+\.?\d*", i)
            print(num)
            num[0] = {"minimum": num[0]}
            num[1] = {"average": num[1]}
            data.get("clear").get("python").update(
                {"Totals": num[-2:]}
            )


def clr_from_golang(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[golang] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Golang-Server\n")]:

        if i.startswith("BenchmarkBuild"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkBuild": num[0][:-6]}
            )

        if i.startswith("BenchmarkGarbage"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkGarbage": num[0][:-6]}
            )

        if i.startswith("BenchmarkHTTP"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkHTTP": num[0][:-6]}
            )

        if i.startswith("BenchmarkJSON"):
            num = re.findall("\d+\.?\d* ns/op", i)
            data.get("clear").get("golang").update(
                {"BenchmarkJSON": num[0][:-6]}
            )


def clr_from_nodejs(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[node] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Node-Server\n")]:

        if i.startswith("Score"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("node").update(
                {"benchmark-node-octane": num[-1]}
            )


def clr_from_openjdk(lines):
    """perl unit tests analysis"""
    for i in lines[
             lines.index("[openjdk] [INFO] Test clear docker image:\n"):
             lines.index("[openjdk] [INFO] Test extra official docker image, official latest image:\n")]:

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("openjdk").update(
                {"MyBenchmark.testMethod.Score": num[-2]})

        if i.startswith("MyBenchmark.testMethod"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("openjdk").update(
                {"MyBenchmark.testMethod.Error": num[-1]})

    # for item in lines:
    #     if item.startswith("[openjdk] [INFO] Test clear docker image:\n"):
    #         start = lines.index(item)
    #
    # for i in lines[start:]:
    #     if i.startswith("Benchmark"):
    #         end = lines[start:].index(i) + start
    #
    # if i in lines[start:end]:
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Score": num[-2]}
    #         )
    #
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Error": num[-1]}
    #         )
    # for i in lines[lines.index("[openjdk] [INFO] Test clear docker image:\n"):]:
    #
    #     i.strip()
    #
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Score": num[-2]}
    #         )
    #
    #     if i.startswith("MyBenchmark.testMethod"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("openjdk").update(
    #             {"MyBenchmark.testMethod.Error": num[-1]}
    #         )


def clr_from_ruby(lines):
    """ruby unit tests analysis"""
    newlines = lines[
               lines.index("[ruby] [INFO] Test extra official docker image, 2.7.0:\n"):
               lines.index("Latest_Official\n")].copy()

    line_str_key = "Calculating"
    line_dict = {}
    ret_lines = []
    for i in range(0, len(newlines)):
        line_dict[i] = newlines[i].split("\n")[0]

    for lineno, line_str in line_dict.items():
        if line_str.startswith(line_str_key):
            # print(lineno, ":", line_str)
            tmp_line_no = lineno + 1
            while True:
                if newlines[tmp_line_no] != "\n":
                    if "so_k_nucleotidepreparing" in newlines[tmp_line_no]:
                        ret_lines.append("so_k_nucleotidepreparing " + newlines[tmp_line_no + 1])
                    if "so_reverse_complementpreparing" in newlines[tmp_line_no]:
                        ret_lines.append("so_reverse_complementpreparing " + newlines[tmp_line_no + 1])
                    ret_lines.append(newlines[tmp_line_no])
                else:
                    break
                tmp_line_no += 1

    ret_line_list = []
    for line in ret_lines:
        # print(line)
        line_split = line.split()
        key_str = line_split[0]
        value = line_split[1]
        if "Time" in line:
            time_line_split = line.split("s -")[0].split(")")
            # print(time_line_split)
            time_key = time_line_split[0].strip() + ")"
            time_value = time_line_split[-1].strip()
            # print(time_value)
            ret_line_list.append({time_key: time_value})
        elif not value.startswith("/"):
            # print(value)
            try:
                key_str = float(str(key_str))
            except Exception:
                pass
            if not isinstance(key_str, float):
                ret_line_list.append({key_str: value})
    # print(len(ret_line_list))
    for tmp_dict in ret_line_list:
        data.get("clear").get("ruby").update(tmp_dict)
    # influs_list = ["app_answer", "app_aobench", "app_erb", "app_factorial",
    #                "app_fib", "app_lc_fizzbuzz", "app_mandelbrot", "app_pentomino",
    #                "app_raise", "app_strconcat", "app_tak", "app_tarai", "app_uri",
    #                "array_sample_100k_10", "array_sample_100k_11", "array_sample_100k__100",
    #                "array_sample_100k__1k", "array_sample_100k__6k", "array_sample_100k___10k",
    #                "array_sample_100k___50k", "array_shift", "array_small_and", "array_small_diff",
    #                "array_small_or", "array_sort_block", "array_sort_float", "array_values_at_int",
    #                "array_values_at_range", "bighash", "complex_float_add", "complex_float_div",
    #                "complex_float_mul", "complex_float_new", "complex_float_power", "complex_float_sub",
    #                "dir_empty_p", "enum_lazy_grep_v_100", "enum_lazy_grep_v_20", "enum_lazy_grep_v_50",
    #                "enum_lazy_uniq_100", "enum_lazy_uniq_20", "enum_lazy_uniq_50", "erb_render",
    #                "fiber_chain", "file_chmod", "file_rename", "hash_aref_dsym", "hash_aref_dsym_long",
    #                "hash_aref_fix", "hash_aref_flo", "hash_aref_miss", "hash_aref_str", "hash_aref_sym",
    #                "hash_aref_sym_long", "hash_flatten", "hash_ident_flo", "hash_ident_num", "hash_ident_obj",
    #                "hash_ident_str", "hash_ident_sym", "hash_keys", "hash_literal_small2", "hash_literal_small4",
    #                "hash_literal_small8", "hash_long", "hash_shift", "hash_shift_u16", "hash_shift_u24",
    #                "hash_shift_u32", "hash_small2", "hash_small4", "hash_small8", "hash_to_proc",
    #                "hash_values", "int_quo", "io_copy_stream_write", "io_copy_stream_write_socket",
    #                "io_file_create", "io_file_read", "io_file_write", "io_nonblock_noex", "io_nonblock_noex2",
    #                "io_pipe_rw", "io_select", "io_select2", "io_select3", "loop_for", "loop_generator",
    #                "loop_times", "loop_whileloop", "loop_whileloop2", "marshal_dump_flo", "marshal_dump_load_geniv",
    #                "marshal_dump_load_time",
    #                "Calculating-(1..1_000_000).last(100)",
    #                "Calculating-(1..1_000_000).last(1000)",
    #                "Calculating-(1..1_000_000).last(10000)",
    #                "capitalize-1",
    #                "capitalize-10",
    #                "capitalize-100",
    #                "capitalize-1000",
    #                "downcase-1",
    #                "downcase-10",
    #                "downcase-100",
    #                "downcase-1000",
    #                "require", "require_thread", "securerandom", "so_ackermann",
    #                "so_array", "so_binary_trees", "so_concatenate", "so_count_words", "so_exception", "so_fannkuch",
    #                "so_fasta", "so_k_nucleotidepreparing", "so_lists", "so_mandelbrot", "so_matrix",
    #                "so_meteor_contest",
    #                "so_nbody", "so_nested_loop", "so_nsieve", "so_nsieve_bits", "so_object", "so_partial_sums",
    #                "so_pidigits", "so_random", "so_reverse_complementpreparing", "so_sieve", "so_spectralnorm",
    #                "string_index", "string_scan_re",
    #                "string_scan_str",
    #                "to_chars-1",
    #                "to_chars-10",
    #                "to_chars-100",
    #                "to_chars-1000",
    #                "swapcase-1",
    #                "swapcase-10",
    #                "swapcase-100",
    #                "swapcase-1000",
    #                "upcase-1",
    #                "upcase-10",
    #                "upcase-100",
    #                "upcase-1000",
    #                """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""",
    #                """Time.strptime("1", "%s")""",
    #                """Time.strptime("0 +0100", "%s %z")""",
    #                """Time.strptime("0 UTC", "%s %z")""",
    #                """Time.strptime("1.5", "%s.%N")""",
    #                """Time.strptime("1.000000000001", "%s.%N")""",
    #                """Time.strptime("20010203 -0200", "%Y%m%d %z")""",
    #                """Time.strptime("20010203 UTC", "%Y%m%d %z")""",
    #                """Time.strptime("2018-365", "%Y-%j")""",
    #                """Time.strptime("2018-091", "%Y-%j")""",
    #                "time_subsec", "vm1_attr_ivar",
    #                "vm1_attr_ivar_set",
    #                "vm1_block", "vm1_blockparam", "vm1_blockparam_call", "vm1_blockparam_pass",
    #                "vm1_blockparam_yield",
    #                "vm1_const", "vm1_ensure", "vm1_float_simple", "vm1_gc_short_lived",
    #                "vm1_gc_short_with_complex_long",
    #                "vm1_gc_short_with_long", "vm1_gc_short_with_symbol", "vm1_gc_wb_ary", "vm1_gc_wb_ary_promoted",
    #                "vm1_gc_wb_obj", "vm1_gc_wb_obj_promoted", "vm1_ivar", "vm1_ivar_set", "vm1_length",
    #                "vm1_lvar_init",
    #                "vm1_lvar_set", "vm1_neq", "vm1_not", "vm1_rescue", "vm1_simplereturn", "vm1_swap", "vm1_yield",
    #                "vm2_array", "vm2_bigarray", "vm2_bighash", "vm2_case", "vm2_case_lit", "vm2_defined_method",
    #                "vm2_dstr", "vm2_eval", "vm2_fiber_switch", "vm2_freezestring", "vm2_method",
    #                "vm2_method_missing",
    #                "vm2_method_with_block", "vm2_module_ann_const_set", "vm2_module_const_set", "vm2_mutex",
    #                "vm2_newlambda",
    #                "vm2_poly_method", "vm2_poly_method_ov", "vm2_poly_singleton", "vm2_proc", "vm2_raise1",
    #                "vm2_raise2",
    #                "vm2_regexp", "vm2_send", "vm2_string_literal", "vm2_struct_big_aref_hi",
    #                "vm2_struct_big_aref_lo",
    #                "vm2_struct_big_aset", "vm2_struct_big_href_hi", "vm2_struct_big_href_lo", "vm2_struct_big_hset",
    #                "vm2_struct_small_aref", "vm2_struct_small_aset", "vm2_struct_small_href",
    #                "vm2_struct_small_hset",
    #                "vm2_super", "vm2_unif1", "vm2_zsuper", "vm3_backtrace", "vm3_clearmethodcache", "vm3_gc",
    #                "vm3_gc_old_full",
    #                "vm3_gc_old_immediate", "vm3_gc_old_lazy", "vm_symbol_block_pass", "vm_thread_alive_check1",
    #                "vm_thread_close",
    #                "vm_thread_condvar1", "vm_thread_condvar2", "vm_thread_create_join", "vm_thread_mutex1",
    #                "vm_thread_mutex2",
    #                "vm_thread_mutex3", "vm_thread_pass", "vm_thread_pass_flood", "vm_thread_pipe",
    #                "vm_thread_queue",
    #                "vm_thread_sized_queue", "vm_thread_sized_queue2", "vm_thread_sized_queue3",
    #                "vm_thread_sized_queue4"
    #                ]
    #
    # data_ruby = {}
    # for i in lines[
    #          lines.index("[ruby] [INFO] Test clear docker image:\n"):
    #          lines.index("Clr-Ruby-Server\n")]:
    #
    #     for startwith_item in influs_list:
    #         # if i.startswith(startwith_item) or i.startswith("\t") and startwith_item in i:
    #         if i.endswith("s/i)\n") and startwith_item in i:
    #             num = re.findall("\d+\.?\d* s|ERROR", i)
    #             data_ruby.update({startwith_item: num[-1][:-1]})
    #
    #     if "so_reverse_complementpreparing" in i:
    #         start = lines.index(i)
    #         so_reverse_complementpreparing = lines[start + 1]
    #         num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
    #         data_ruby.update({"so_reverse_complementpreparing": num[-1][:-1]})
    #
    #     if "so_k_nucleotidepreparing" in i:
    #         start = lines.index(i)
    #         so_reverse_complementpreparing = lines[start + 1]
    #         num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
    #         data_ruby.update({"so_k_nucleotidepreparing": num[-1][:-1]})
    #
    # lines = lines[
    #         lines.index("[ruby] [INFO] Test clear docker image:\n"):
    #         lines.index("Clr-Ruby-Server\n")]
    #
    # for item in lines:
    #     if item.startswith("Warming up --------------------------------------\n"):
    #         up = lines.index(item)
    #
    # for item in lines[up:]:
    #     if item.startswith("Comparison:\n"):
    #         down = lines[up:].index(item) + up
    #
    # for i in lines[up:down]:
    #
    #     if "(1..1_000_000).last(100)" in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"(1..1_000_000).last(100)": num[-4]})
    #
    #     if "(1..1_000_000).last(1000)" in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"(1..1_000_000).last(1000)": num[-4]})
    #
    #     if "(1..1_000_000).last(10000)" in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"(1..1_000_000).last(10000)": num[-4]})
    #
    # for i in lines[down:]:
    #
    #     if i.startswith("Warming up --------------------------------------\n"):
    #         capit_start = lines[down:].index(i) + down
    #
    # for i in lines[capit_start:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         calc_start = lines[capit_start:].index(i) + capit_start
    #
    # for i in lines[calc_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         calc_end = lines[calc_start:].index(i) + calc_start
    #
    # for i in lines[calc_start:calc_end]:
    #
    #     if "capitalize-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-1": num[1]})
    #
    #     if "capitalize-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-10": num[1]})
    #
    #     if "capitalize-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-100": num[1]})
    #
    #     if "capitalize-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"capitalize-1000": num[1]})
    #
    # for i in lines[calc_end:]:
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         downcase_start = lines[calc_end:].index(i) + calc_end
    #
    # for i in lines[downcase_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         downcase_end = lines[downcase_start:].index(i) + downcase_start
    #
    # for i in lines[downcase_start:downcase_end]:
    #
    #     if "downcase-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-1": num[1]})
    #
    #     if "downcase-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-10": num[1]})
    #
    #     if "downcase-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-100": num[1]})
    #
    #     if "downcase-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"downcase-1000": num[1]})
    #
    # for i in lines[downcase_end:]:
    #     if i.startswith("Warming up --------------------------------------\n"):
    #         to_chars = lines[downcase_end:].index(i) + downcase_end
    #
    # for i in lines[to_chars:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         to_chars_start = lines[to_chars:].index(i) + to_chars
    #
    # for i in lines[to_chars_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         to_chars_end = lines[to_chars_start:].index(i) + to_chars_start
    #
    # for i in lines[to_chars_start:to_chars_end]:
    #
    #     if "to_chars-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-1": num[1]})
    #
    #     if "to_chars-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-10": num[1]})
    #
    #     if "to_chars-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-100": num[1]})
    #
    #     if "to_chars-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"to_chars-1000": num[1]})
    #
    # for i in lines[to_chars_end:]:
    #
    #     if i.startswith("Warming up --------------------------------------\n"):
    #         swapcase = lines[to_chars_end:].index(i) + to_chars_end
    #
    # for i in lines[swapcase:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         swapcase_start = lines[swapcase:].index(i) + swapcase
    #
    # for i in lines[swapcase_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         swapcase_end = lines[swapcase_start:].index(i) + swapcase_start
    #
    # for i in lines[swapcase_start:swapcase_end]:
    #
    #     if "swapcase-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-1": num[1]})
    #
    #     if "swapcase-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-10": num[1]})
    #
    #     if "swapcase-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-100": num[1]})
    #
    #     if "swapcase-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"swapcase-1000": num[1]})
    #
    # for i in lines[swapcase_end:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         upcase_start = lines[swapcase_end:].index(i) + swapcase_end
    #
    # for i in lines[upcase_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         upcase_end = lines[upcase_start:].index(i) + upcase_start
    #
    # for i in lines[upcase_start:upcase_end]:
    #
    #     if "upcase-1  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-1": num[1]})
    #
    #     if "upcase-10  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-10": num[1]})
    #
    #     if "upcase-100  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-100": num[1]})
    #
    #     if "upcase-1000  " in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"upcase-1000": num[1]})
    #
    # for i in lines[upcase_end:]:
    #
    #     if i.startswith("Calculating -------------------------------------\n"):
    #         time_start = lines[upcase_end:].index(i) + upcase_end
    #
    # for i in lines[time_start:]:
    #
    #     if i.startswith("Comparison:\n"):
    #         time_end = lines[time_start:].index(i) + time_start
    #
    # for i in lines[time_start:time_end]:
    #
    #     if """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""": num[-4]})
    #
    #     if """Time.strptime("1", "%s")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("1", "%s")""": num[-4]})
    #
    #     if """Time.strptime("0 +0100", "%s %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("0 +0100", "%s %z")""": num[-4]})
    #
    #     if """Time.strptime("0 UTC", "%s %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("0 UTC", "%s %z")""": num[-4]})
    #
    #     if """Time.strptime("1.5", "%s.%N")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("1.5", "%s.%N")""": num[-4]})
    #
    #     if """Time.strptime("1.000000000001", "%s.%N")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("1.000000000001", "%s.%N")""": num[-4]})
    #
    #     if """Time.strptime("20010203 -0200", "%Y%m%d %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("20010203 -0200", "%Y%m%d %z")""": num[-4]})
    #
    #     if """Time.strptime("20010203 UTC", "%Y%m%d %z")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("20010203 UTC", "%Y%m%d %z")""": num[-4]})
    #
    #     if """Time.strptime("2018-365", "%Y-%j")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("2018-365", "%Y-%j")""": num[-4]})
    #
    #     if """Time.strptime("2018-091", "%Y-%j")  """ in i:
    #         num = re.findall("\d+\.?\d*", i)
    #         data_ruby.update({"""Time.strptime("2018-091", "%Y-%j")""": num[-4]})
    #
    # data.get("clear").get("ruby").update(data_ruby)

    # for item in lines:
    #     if item.startswith("[perl] [INFO] Test clear docker image:\n"):
    #         start = lines.index(item)
    #
    # for i in lines[start:]:
    #     if i.startswith("Test: benchmarks/startup/noprog.b"):
    #         end = lines[start:].index(i) + start
    #
    # for item in lines[start:end]:
    #     if item.startswith("Test-File: benchmarks/app/podhtml.b\n"):
    #         up = lines[start:end].index(item) + start
    #
    #     if item.startswith("Test: benchmarks/startup/noprog.b"):
    #         down = lines[start:end].index(item) + start
    #
    # for i in lines[up:down]:
    #     if i.startswith("Avg"):
    #         num = re.findall("\d+\.?\d*", i)
    #         data.get("clear").get("perl").update(
    #             {"podhtml.b": num[0]}
    #         )
    #
    # for item in lines[start:end]:
    #     if item.startswith("Test: benchmarks/startup/noprog.b"):
    #         up = lines[start:end].index(item) + start
    #
    #     if item.startswith("Test: benchmarks/statement/assign-int.b"):
    #         down = lines[start:end].index(item) + start
    #
    # for i in lines[up:down]:
    #     if i.startswith("Avg:"):
    #         num = re.findall("\d+\.\d*", i)
    #         data.get("clear").get("perl").update(
    #             {"noprog.b": num[0]}
    #         )


def DEFAULT_RUBY(lines):
    # filename = r"C:\Users\xinhuizx\Intel-Test-MQservice\test_ruby.log"
    # newlines = []
    # with open(filename) as f:
    #     for line in f.readlines():
    #         # newlines.append(line.split("\n")[0])
    #         newlines.append(line)

    newlines = lines[
               lines.index("[ruby] [INFO] Test docker hub official image first:\n"):
               lines.index("[ruby] [INFO] Test clear docker image:\n")].copy()

    line_str_key = "Calculating"
    line_dict = {}
    ret_lines = []
    for i in range(0, len(newlines)):
        line_dict[i] = newlines[i].split("\n")[0]

    for lineno, line_str in line_dict.items():
        if line_str.startswith(line_str_key):
            # print(lineno, ":", line_str)
            tmp_line_no = lineno + 1
            while True:
                if newlines[tmp_line_no] != "\n":
                    if "so_k_nucleotidepreparing" in newlines[tmp_line_no]:
                        ret_lines.append("so_k_nucleotidepreparing " + newlines[tmp_line_no + 1])
                    if "so_reverse_complementpreparing" in newlines[tmp_line_no]:
                        ret_lines.append("so_reverse_complementpreparing " + newlines[tmp_line_no + 1])
                    ret_lines.append(newlines[tmp_line_no])
                else:
                    break
                tmp_line_no += 1

    ret_line_list = []
    for line in ret_lines:
        # print(line)
        line_split = line.split()
        key_str = line_split[0]
        value = line_split[1]
        if "Time" in line:
            time_line_split = line.split("s -")[0].split(")")
            # print(time_line_split)
            time_key = time_line_split[0].strip() + ")"
            time_value = time_line_split[-1].strip()
            # print(time_value)
            ret_line_list.append({time_key: time_value})
        elif not value.startswith("/"):
            # print(value)
            try:
                key_str = float(str(key_str))
            except Exception:
                pass
            if not isinstance(key_str, float):
                ret_line_list.append({key_str: value})
    print(len(ret_line_list))
    for tmp_dict in ret_line_list:
        data.get("clear").get("ruby").update(tmp_dict)


def clr_from_postgres(lines):
    """perl unit test analysis"""
    lines_b = lines[lines.index("[postgres] [INFO] Test clear docker image:\n"):].copy()
    # lines_b = lines[
    #           lines.index("[postgres] [INFO] Test clear docker image:\n"):
    #           lines.index("[postgres] [INFO] Test extra official docker image, postgres9.6:\n")].copy()

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
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE": bhw2[2]}
    )
    data.get("clear").get("postgres").update(
        {"BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY": bhr2[2]}
    )


def clr_from_tensorflow(lines):
    """clearlinux unit tests analysis"""

    for i in lines[
             lines.index("[tensorflow] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Tensorflow-Server\n")]:

        if i.startswith("Total duration"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("tensorflow").update(
                {"Total duration": num[0]})


def clr_from_mariadb(lines):
    """mariadb unit tests analysis"""
    for i in lines[
             lines.index("[mariadb] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Mariadb\n")]:

        i = i.strip()
        if i.startswith("Average number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("mariadb").update(
                {"Average number of seconds to run all queries": num[0]}
            )

        if i.startswith("Minimum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("mariadb").update(
                {"Minimum number of seconds to run all queries": num[0]}
            )

        if i.startswith("Maximum number of seconds"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("mariadb").update(
                {"Maximum number of seconds to run all queries": num[0]}
            )


def clr_from_flink(lines):
    """flink unit tests analysis"""

    for i in lines[
             lines.index("[flink] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Flink-Server\n")]:

        if i.startswith("KeyByBenchmarks.arrayKeyBy"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"KeyByBenchmarks.arrayKeyBy": num[-2]})

        if i.startswith("KeyByBenchmarks.tupleKeyBy"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"KeyByBenchmarks.tupleKeyBy": num[-2]})

        if i.startswith("MemoryStateBackendBenchmark.stateBackends") and "MEMORY" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"MemoryStateBackendBenchmark.stateBackends-MEMORY": num[-2]})

        if i.startswith("MemoryStateBackendBenchmark.stateBackends") and " FS " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"MemoryStateBackendBenchmark.stateBackends-FS": num[-2]})

        if i.startswith("MemoryStateBackendBenchmark.stateBackends") and "_ASYNC " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"MemoryStateBackendBenchmark.stateBackends-FS_ASYNC": num[-2]})

        if i.startswith("RocksStateBackendBenchmark.stateBackends") and " ROCKS " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"RocksStateBackendBenchmark.stateBackends-ROCKS": num[-2]})

        if i.startswith("RocksStateBackendBenchmark.stateBackends") and "_INC " in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"RocksStateBackendBenchmark.stateBackends-ROCKS_INC": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerAvro"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerAvro": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerKryo"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerKryo": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerPojo"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerPojo": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerRow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerRow": num[-2]})

        if i.startswith("SerializationFrameworkMiniBenchmarks.serializerTuple"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"SerializationFrameworkMiniBenchmarks.serializerTuple": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1,100ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1,100ms": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "100,1ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-100,1ms": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1000,1ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,1ms": num[-2]})

        if i.startswith("StreamNetworkThroughputBenchmarkExecutor.networkThroughput") and "1000,100ms" in i:
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,100ms": num[-2]})

        if i.startswith("SumLongsBenchmark.benchmarkCount"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"SumLongsBenchmark.benchmarkCount": num[-2]})

        if i.startswith("WindowBenchmarks.globalWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"WindowBenchmarks.globalWindow": num[-2]})

        if i.startswith("WindowBenchmarks.sessionWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"WindowBenchmarks.sessionWindow": num[-2]})

        if i.startswith("WindowBenchmarks.slidingWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"WindowBenchmarks.slidingWindow": num[-2]})

        if i.startswith("WindowBenchmarks.tumblingWindow"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"WindowBenchmarks.tumblingWindow": num[-2]})

        if i.startswith("StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1"):
            num = re.findall("\d+\.?\d*", i)
            data.get("clear").get("flink").update(
                {"StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1": num[-2]})


"""STATUS_default_log"""


def StaDefHttpd(lines):
    """default test_status_httpd long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("httpd"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:
        if i.startswith("httpd"):
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


def StaDefNginx(lines):
    """default test_status_nginx long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("nginx"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("nginx"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("nginx").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("nginx").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("nginx").update(
                {"MicroService_layer": num[0]}
            )


def StaDefMemcached(lines):
    """default test_status_nginx long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("memcached"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("memcached"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("memcached").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("memcached").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("memcached").update(
                {"MicroService_layer": num[0]}
            )


def StaDefRedis(lines):
    """default test_status_redis long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("redis"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("redis"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("redis").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("redis").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("redis").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPhp(lines):
    """default test_status_php long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("php"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("php"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("php").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("php").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("php").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPython(lines):
    """default test_status_python long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("python"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("python"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("python").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("python").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("python").update(
                {"MicroService_layer": num[0]}
            )


def StaDefGolang(lines):
    """default test_status_golang long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("golang"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("golang"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("golang").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("golang").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("golang").update(
                {"MicroService_layer": num[0]}
            )


def StaDefNode(lines):
    """"default test_status_node log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("node"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("node"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("node").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("node").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("node").update(
                {"MicroService_layer": num[0]}
            )


def StaDefOpenjdk(lines):
    """default test_status_openjdk log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("openjdk"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("openjdk"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("openjdk").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("openjdk").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("openjdk").update(
                {"MicroService_layer": num[0]}
            )


def StaDefRuby(lines):
    """clearlinux test_status_ruby log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("ruby"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("ruby"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("ruby").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("ruby").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("ruby").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPerl(lines):
    """clearlinux test_status_perl log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("perl"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:
        if i.startswith("perl"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("perl").update(
                    {"Toatl": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("perl").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("perl").update(
                {"MicroService_layer": num[0]}
            )


def StaDefTensorflow(lines):
    """default test_status_tensorflow log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("tensorflow"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("tensorflow"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("tensorflow").update(
                    {"Total": num[-1] + "GB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("tensorflow").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("tensorflow").update(
                {"MicroService_layer": num[0]}
            )


def StaDefPostgres(lines):
    """default test_status_postgres long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("postgres"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("postgres"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("postgres").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("postgres").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("postgres").update(
                {"MicroService_layer": num[0]}
            )


def StaDefMariadb(lines):
    """default test_status_postgres long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("mariadb"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("mariadb"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("mariadb").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("mariadb").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("mariadb").update(
                {"MicroService_layer": num[0]}
            )


def StaDefRabbitmq(lines):
    """default test_status_perl log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("rabbitmq"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("rabbitmq"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_def").get("rabbitmq").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("default base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("rabbitmq").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("default microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_def").get("rabbitmq").update(
                {"MicroService_layer": num[0]}
            )


"""STATUS_clearlinux_log"""


def StaClrHttpd(lines):
    """clearlinux test_status_httpd long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("httpd"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/httpd"):
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


def StaClrNginx(lines):
    """clearlinux test_status_nginx long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("nginx"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/nginx"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("nginx").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("nginx").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("nginx").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/nginx version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("nginx").update(
                {"VERSION_ID": num[0]}
            )


def StaClrMemcached(lines):
    """clearlinux test_status_nginx long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("memcached"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/memcached"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("memcached").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("memcached").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("memcached").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/memcached version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("memcached").update(
                {"VERSION_ID": num[0]}
            )


def StaClrRedis(lines):
    """default test_status_redis long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("redis"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/redis"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("redis").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("redis").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("redis").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/redis version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("redis").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPhp(lines):
    """default test_status_php long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("php"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/php"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("php").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("php").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("php").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/php version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("php").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPython(lines):
    """clearlinux test_status_python long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("python"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/python"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("python").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("python").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("python").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/python version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("python").update(
                {"VERSION_ID": num[0]}
            )


def StaClrGolang(lines):
    """clearlinux test_status_golang long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("golang"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/golang"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("golang").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("golang").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("golang").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/golang version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("golang").update(
                {"VERSION_ID": num[0]}
            )


def StaClrNode(lines):
    """default test_status_node long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("node"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/node"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("node").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("node").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("node").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/node version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("node").update(
                {"VERSION_ID": num[0]}
            )


def StaClrOpenjdk(lines):
    """clearlinux test_status_openjdk long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("openjdk"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/openjdk"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("openjdk").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("openjdk").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("openjdk").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/openjdk version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("openjdk").update(
                {"VERSION_ID": num[0]}
            )


def StaClrRuby(lines):
    """clearlinux test_status_openjdk long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("ruby"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/ruby"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("ruby").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("ruby").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("ruby").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/ruby version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("ruby").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPerl(lines):
    """clearlinux test_status_perl log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("perl"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/perl"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("perl").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("perl").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("perl").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/perl version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("perl").update(
                {"VERSION_ID": num[0]}
            )


def StaClrTensorflow(lines):
    """clearlinux test_status_tensorflow log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("tensorflow"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/tensorflow"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("tensorflow").update(
                    {"Total": num[-1] + "GB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("tensorflow").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("tensorflow").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/tensorflow version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("tensorflow").update(
                {"VERSION_ID": num[0]}
            )


def StaClrPostgres(lines):
    """default test_status_postgres long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("postgres"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/postgres"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("postgres").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("postgres").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("postgres").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/postgres version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("postgres").update(
                {"VERSION_ID": num[0]}
            )


def StaClrMariadb(lines):
    """default test_status_mariadb long analysis"""

    if_n = True
    for i in lines:
        if i.startswith("mariadb"):
            if "latest" in i:
                start = lines.index(i)
                # print(start)

    while if_n:
        for i in lines[start:]:
            if i == '\n':
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/mariadb"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("mariadb").update(
                    {"Total": num[-1] + "MB"}
                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("mariadb").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("mariadb").update(
                {"MicroService_layer": num[0]})

    for i in lines[start:]:
        if i.startswith("clearlinux/mariadb version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("mariadb").update(
                {"VERSION_ID": num[0]}
            )


def StaClrRabbitmq(lines):
    """clearlinux test_status_perl log analysis"""

    if_n = True
    for i in lines:
        if i.startswith("rabbitmq"):
            if "latest" in i:
                start = lines.index(i)

    while if_n:
        for i in lines[start:]:
            if i == "\n":
                if_n = False
                end = lines[start:].index(i)

    for i in lines[start:end + start]:

        if i.startswith("clearlinux/rabbitmq"):
            if "latest" in i:
                num = re.findall("\d+\.?\d*", i)
                data.get("status_Clr").get("rabbitmq").update(
                    {"Total": num[-1] + "GB"}

                )

        if i.startswith("clearlinux base layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("rabbitmq").update(
                {"Base_Layer": num[0]}
            )

        if i.startswith("clearlinux microservice added layer Size:"):
            num = re.findall("\d+\.?\d*", i)
            data.get("status_Clr").get("rabbitmq").update(
                {"MicroService_layer": num[0]}
            )

    for i in lines[start:]:
        if i.startswith("clearlinux/perl version:\n"):
            end = lines[start:].index(i) + 1
            num = re.findall("\d+\.?\d*", lines[start:][end])
            data.get("status_Clr").get("rabbitmq").update(
                {"VERSION_ID": num[0]}
            )


def main():
    file_name = r"C:\Users\xinhuizx\Intel-Test-MQservice\log\2019-08-05-Clr\test_log\python\2019-08-05-19_20_49.log"
    test = read_logs(file_name)

    status_log = r"C:\Users\xinhuizx\Intel-Test-MQservice\log\2019-08-05-Clr\status_log\2019-08-05-11_50_55.log"
    status = read_status_logs(status_log)

    # default_from_httpd(test)
    # default_from_nginx(test)
    # default_from_memcached(test)
    # default_from_redis(test)
    # default_from_php(test)
    default_from_python(test)
    # default_from_golang(test)
    # default_from_nodejs(test)
    # default_from_openjdk(test)
    # default_from_ruby(test)
    # default_from_postgres(test)
    # default_from_tensorflow(test)
    # default_from_mariadb(test)
    # default_from_ruby(test)
    # default_from_flink(test)
    # DEFAULT_RUBY(test)

    # clr_from_httpd(test)
    # clr_from_nginx(test)
    # clr_from_memcached(test)
    # clr_from_redis(test)
    # clr_from_php(test)
    # clr_from_golang(test)
    clr_from_python(test)
    # clr_from_nodejs(test)
    # clr_from_openjdk(test)
    # clr_from_ruby(test)
    # clr_from_postgres(test)
    # clr_from_tensorflow(test)
    # clr_from_mariadb(test)
    # clr_from_ruby(test)
    # clr_from_flink(test)

    # StaDefHttpd(status)
    # StaDefRuby(status)
    # StaDefNginx(status)
    # StaDefMemcached(status)
    # StaDefRedis(status)
    # StaDefPhp(status)
    # StaDefPython(status)
    # StaDefGolang(status)
    # StaDefNode(status)
    # StaDefOpenjdk(status)
    # StaDefPerl(status)
    # StaDefTensorflow(status)
    # StaDefPostgres(status)
    # StaDefMariadb(status)
    # StaDefRabbitmq(status)
    # StaDefRuby(status)

    # StaClrHttpd(status)
    # StaClrNginx(status)
    # StaClrMemcached(status)
    # StaClrRedis(status)
    # StaClrPhp(status)
    # StaClrPython(status)
    # StaClrGolang(status)
    # StaClrNode(status)
    # StaClrOpenjdk(status)
    # StaClrRuby(status)
    # StaClrPerl(status)
    # StaClrTensorflow(status)
    # StaClrPostgres(status)
    # StaClrMariadb(status)
    # StaClrRabbitmq(status)
    # StaClrRuby(status)

    # with open(r'C:\Users\xinhuizx\Intel-Test-MQservice\json\data_New_4.json', "w") as f:
    #     json.dump(data, f)


if __name__ == '__main__':
    main()
    pprint(data)

"""
test_cmd = ["make httpd", "make nginx", "make memcached", "make redis", "make php", "make python", "make node",
            "make golang", "make postgres", "make tensorflow", "make mariadb", "make perl", "make openjdk",
            "make rabbitmq", "make flink", "make cassandra","make ruby"]



test_cmd = ["make golang", "make tensorflow", "make perl", "make postgres", "make ruby", "make flink"]
"""
