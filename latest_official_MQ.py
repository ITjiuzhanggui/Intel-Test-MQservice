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


def read_logs(file_name):
    with open(file_name, 'r', encoding="utf-8")as f:
        return f.readlines()


def read_status_logs(status_log):
    with open(status_log, 'r', encoding="utf-8")as s:
        return s.readlines()


def Log_openjdk(lines):
    """analysis openjdk test log"""

    for i in lines[
             lines.index("[openjdk] [INFO] Test extra official docker image, official latest image:\n"):
             lines.index("Latest_Official\n")]:

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

    """clearlinux openjdk test log analysis"""
    # for i in lines[
    #          lines.index("[openjdk] [INFO] Test clear docker image:\n"):
    #          lines.index("[openjdk] [INFO] Test extra official docker image, official latest image:\n")]:
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


def Log_postgres(lines):
    """analysis postgres test log"""

    lines_a = lines[lines.index("[postgres] [INFO] Test extra official docker image, postgres9.6:\n"):].copy()
    line_nu = []
    for i in lines_a:
        if re.search(r"excluding", i) != None:
            line_nu.append(lines_a.index(i))
    # pprint(line_nu)
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

    """clearlinux openjdk test log analysis"""

    lines_b = lines[
              lines.index("[postgres] [INFO] Test clear docker image:\n"):
              lines.index("[postgres] [INFO] Test extra official docker image, postgres9.6:\n")].copy()
    line_nu2 = []
    for i in lines_b:
        if re.search(r"excluding", i) != None:
            line_nu2.append(lines_b.index(i))
        # pprint(line_nu2)
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


def Log_ruby(lines):
    """analysis ruby test log"""

    influs_list = ["app_answer", "app_aobench", "app_erb", "app_factorial",
                   "app_fib", "app_lc_fizzbuzz", "app_mandelbrot", "app_pentomino",
                   "app_raise", "app_strconcat", "app_tak", "app_tarai", "app_uri",
                   "array_sample_100k_10", "array_sample_100k_11", "array_sample_100k__100",
                   "array_sample_100k__1k", "array_sample_100k__6k", "array_sample_100k___10k",
                   "array_sample_100k___50k", "array_shift", "array_small_and", "array_small_diff",
                   "array_small_or", "array_sort_block", "array_sort_float", "array_values_at_int",
                   "array_values_at_range", "bighash", "complex_float_add", "complex_float_div",
                   "complex_float_mul", "complex_float_new", "complex_float_power", "complex_float_sub",
                   "dir_empty_p", "enum_lazy_grep_v_100", "enum_lazy_grep_v_20", "enum_lazy_grep_v_50",
                   "enum_lazy_uniq_100", "enum_lazy_uniq_20", "enum_lazy_uniq_50", "erb_render",
                   "fiber_chain", "file_chmod", "file_rename", "hash_aref_dsym", "hash_aref_dsym_long",
                   "hash_aref_fix", "hash_aref_flo", "hash_aref_miss", "hash_aref_str", "hash_aref_sym",
                   "hash_aref_sym_long", "hash_flatten", "hash_ident_flo", "hash_ident_num", "hash_ident_obj",
                   "hash_ident_str", "hash_ident_sym", "hash_keys", "hash_literal_small2", "hash_literal_small4",
                   "hash_literal_small8", "hash_long", "hash_shift", "hash_shift_u16", "hash_shift_u24",
                   "hash_shift_u32", "hash_small2", "hash_small4", "hash_small8", "hash_to_proc",
                   "hash_values", "int_quo", "io_copy_stream_write", "io_copy_stream_write_socket",
                   "io_file_create", "io_file_read", "io_file_write", "io_nonblock_noex", "io_nonblock_noex2",
                   "io_pipe_rw", "io_select", "io_select2", "io_select3", "loop_for", "loop_generator",
                   "loop_times", "loop_whileloop", "loop_whileloop2", "marshal_dump_flo", "marshal_dump_load_geniv",
                   "marshal_dump_load_time",
                   "Calculating-(1..1_000_000).last(100)",
                   "Calculating-(1..1_000_000).last(1000)",
                   "Calculating-(1..1_000_000).last(10000)",
                   "capitalize-1",
                   "capitalize-10",
                   "capitalize-100",
                   "capitalize-1000",
                   "downcase-1",
                   "downcase-10",
                   "downcase-100",
                   "downcase-1000",
                   "require", "require_thread", "securerandom", "so_ackermann",
                   "so_array", "so_binary_trees", "so_concatenate", "so_count_words", "so_exception", "so_fannkuch",
                   "so_fasta", "so_k_nucleotidepreparing", "so_lists", "so_mandelbrot", "so_matrix",
                   "so_meteor_contest",
                   "so_nbody", "so_nested_loop", "so_nsieve", "so_nsieve_bits", "so_object", "so_partial_sums",
                   "so_pidigits", "so_random", "so_reverse_complementpreparing", "so_sieve", "so_spectralnorm",
                   "string_index", "string_scan_re",
                   "string_scan_str",
                   "to_chars-1",
                   "to_chars-10",
                   "to_chars-100",
                   "to_chars-1000",
                   "swapcase-1",
                   "swapcase-10",
                   "swapcase-100",
                   "swapcase-1000",
                   "upcase-1",
                   "upcase-10",
                   "upcase-100",
                   "upcase-1000",
                   """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""",
                   """Time.strptime("1", "%s")""",
                   """Time.strptime("0 +0100", "%s %z")""",
                   """Time.strptime("0 UTC", "%s %z")""",
                   """Time.strptime("1.5", "%s.%N")""",
                   """Time.strptime("1.000000000001", "%s.%N")""",
                   """Time.strptime("20010203 -0200", "%Y%m%d %z")""",
                   """Time.strptime("20010203 UTC", "%Y%m%d %z")""",
                   """Time.strptime("2018-365", "%Y-%j")""",
                   """Time.strptime("2018-091", "%Y-%j")""",
                   "time_subsec", "vm1_attr_ivar",
                   "vm1_attr_ivar_set",
                   "vm1_block", "vm1_blockparam", "vm1_blockparam_call", "vm1_blockparam_pass",
                   "vm1_blockparam_yield",
                   "vm1_const", "vm1_ensure", "vm1_float_simple", "vm1_gc_short_lived",
                   "vm1_gc_short_with_complex_long",
                   "vm1_gc_short_with_long", "vm1_gc_short_with_symbol", "vm1_gc_wb_ary", "vm1_gc_wb_ary_promoted",
                   "vm1_gc_wb_obj", "vm1_gc_wb_obj_promoted", "vm1_ivar", "vm1_ivar_set", "vm1_length",
                   "vm1_lvar_init",
                   "vm1_lvar_set", "vm1_neq", "vm1_not", "vm1_rescue", "vm1_simplereturn", "vm1_swap", "vm1_yield",
                   "vm2_array", "vm2_bigarray", "vm2_bighash", "vm2_case", "vm2_case_lit", "vm2_defined_method",
                   "vm2_dstr", "vm2_eval", "vm2_fiber_switch", "vm2_freezestring", "vm2_method",
                   "vm2_method_missing",
                   "vm2_method_with_block", "vm2_module_ann_const_set", "vm2_module_const_set", "vm2_mutex",
                   "vm2_newlambda",
                   "vm2_poly_method", "vm2_poly_method_ov", "vm2_poly_singleton", "vm2_proc", "vm2_raise1",
                   "vm2_raise2",
                   "vm2_regexp", "vm2_send", "vm2_string_literal", "vm2_struct_big_aref_hi",
                   "vm2_struct_big_aref_lo",
                   "vm2_struct_big_aset", "vm2_struct_big_href_hi", "vm2_struct_big_href_lo", "vm2_struct_big_hset",
                   "vm2_struct_small_aref", "vm2_struct_small_aset", "vm2_struct_small_href",
                   "vm2_struct_small_hset",
                   "vm2_super", "vm2_unif1", "vm2_zsuper", "vm3_backtrace", "vm3_clearmethodcache", "vm3_gc",
                   "vm3_gc_old_full",
                   "vm3_gc_old_immediate", "vm3_gc_old_lazy", "vm_symbol_block_pass", "vm_thread_alive_check1",
                   "vm_thread_close",
                   "vm_thread_condvar1", "vm_thread_condvar2", "vm_thread_create_join", "vm_thread_mutex1",
                   "vm_thread_mutex2",
                   "vm_thread_mutex3", "vm_thread_pass", "vm_thread_pass_flood", "vm_thread_pipe",
                   "vm_thread_queue",
                   "vm_thread_sized_queue", "vm_thread_sized_queue2", "vm_thread_sized_queue3",
                   "vm_thread_sized_queue4"
                   ]

    data_ruby = {}

    for i in lines[
             lines.index("[ruby] [INFO] Test extra official docker image, 2.7.0:\n"):
             lines.index("Latest_Official\n")]:

        for startwith_item in influs_list:
            # if i.startswith(startwith_item) or i.startswith("\t") and startwith_item in i:
            if i.endswith("s/i)\n") and startwith_item in i:
                num = re.findall("\d+\.?\d* s|ERROR", i)
                data_ruby.update({startwith_item: num[-1][:-1]})

        if "so_reverse_complementpreparing" in i:
            start = lines.index(i)
            so_reverse_complementpreparing = lines[start + 1]
            num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
            data_ruby.update({"so_reverse_complementpreparing": num[-1][:-1]})

        if "so_k_nucleotidepreparing" in i:
            start = lines.index(i)
            so_reverse_complementpreparing = lines[start + 1]
            num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
            data_ruby.update({"so_k_nucleotidepreparing": num[-1][:-1]})

    lines = lines[
            lines.index("[ruby] [INFO] Test extra official docker image, 2.7.0:\n"):
            lines.index("Latest_Official\n")]

    for item in lines:
        if item.startswith("Warming up --------------------------------------\n"):
            up = lines.index(item)

    for item in lines[up:]:
        if item.startswith("Comparison:\n"):
            down = lines[up:].index(item) + up

    for i in lines[up:down]:

        if "(1..1_000_000).last(100)" in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"(1..1_000_000).last(100)": num[-4]})

        if "(1..1_000_000).last(1000)" in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"(1..1_000_000).last(1000)": num[-4]})

        if "(1..1_000_000).last(10000)" in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"(1..1_000_000).last(10000)": num[-4]})

    for i in lines[down:]:

        if i.startswith("Warming up --------------------------------------\n"):
            capit_start = lines[down:].index(i) + down

    for i in lines[capit_start:]:

        if i.startswith("Calculating -------------------------------------\n"):
            calc_start = lines[capit_start:].index(i) + capit_start

    for i in lines[calc_start:]:

        if i.startswith("Comparison:\n"):
            calc_end = lines[calc_start:].index(i) + calc_start

    for i in lines[calc_start:calc_end]:

        if "capitalize-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-1": num[1]})

        if "capitalize-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-10": num[1]})

        if "capitalize-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-100": num[1]})

        if "capitalize-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-1000": num[1]})

    for i in lines[calc_end:]:
        if i.startswith("Calculating -------------------------------------\n"):
            downcase_start = lines[calc_end:].index(i) + calc_end

    for i in lines[downcase_start:]:

        if i.startswith("Comparison:\n"):
            downcase_end = lines[downcase_start:].index(i) + downcase_start

    for i in lines[downcase_start:downcase_end]:

        if "downcase-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-1": num[1]})

        if "downcase-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-10": num[1]})

        if "downcase-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-100": num[1]})

        if "downcase-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-1000": num[1]})

    for i in lines[downcase_end:]:
        if i.startswith("Warming up --------------------------------------\n"):
            to_chars = lines[downcase_end:].index(i) + downcase_end

    for i in lines[to_chars:]:

        if i.startswith("Calculating -------------------------------------\n"):
            to_chars_start = lines[to_chars:].index(i) + to_chars

    for i in lines[to_chars_start:]:

        if i.startswith("Comparison:\n"):
            to_chars_end = lines[to_chars_start:].index(i) + to_chars_start

    for i in lines[to_chars_start:to_chars_end]:

        if "to_chars-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-1": num[1]})

        if "to_chars-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-10": num[1]})

        if "to_chars-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-100": num[1]})

        if "to_chars-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-1000": num[1]})

    for i in lines[to_chars_end:]:

        if i.startswith("Warming up --------------------------------------\n"):
            swapcase = lines[to_chars_end:].index(i) + to_chars_end

    for i in lines[swapcase:]:

        if i.startswith("Calculating -------------------------------------\n"):
            swapcase_start = lines[swapcase:].index(i) + swapcase

    for i in lines[swapcase_start:]:

        if i.startswith("Comparison:\n"):
            swapcase_end = lines[swapcase_start:].index(i) + swapcase_start

    for i in lines[swapcase_start:swapcase_end]:

        if "swapcase-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-1": num[1]})

        if "swapcase-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-10": num[1]})

        if "swapcase-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-100": num[1]})

        if "swapcase-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-1000": num[1]})

    for i in lines[swapcase_end:]:

        if i.startswith("Calculating -------------------------------------\n"):
            upcase_start = lines[swapcase_end:].index(i) + swapcase_end

    for i in lines[upcase_start:]:

        if i.startswith("Comparison:\n"):
            upcase_end = lines[upcase_start:].index(i) + upcase_start

    for i in lines[upcase_start:upcase_end]:

        if "upcase-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-1": num[1]})

        if "upcase-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-10": num[1]})

        if "upcase-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-100": num[1]})

        if "upcase-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-1000": num[1]})

    for i in lines[upcase_end:]:

        if i.startswith("Calculating -------------------------------------\n"):
            time_start = lines[upcase_end:].index(i) + upcase_end

    for i in lines[time_start:]:

        if i.startswith("Comparison:\n"):
            time_end = lines[time_start:].index(i) + time_start

    for i in lines[time_start:time_end]:

        if """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""": num[-4]})

        if """Time.strptime("1", "%s")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("1", "%s")""": num[-4]})

        if """Time.strptime("0 +0100", "%s %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("0 +0100", "%s %z")""": num[-4]})

        if """Time.strptime("0 UTC", "%s %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("0 UTC", "%s %z")""": num[-4]})

        if """Time.strptime("1.5", "%s.%N")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("1.5", "%s.%N")""": num[-4]})

        if """Time.strptime("1.000000000001", "%s.%N")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("1.000000000001", "%s.%N")""": num[-4]})

        if """Time.strptime("20010203 -0200", "%Y%m%d %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("20010203 -0200", "%Y%m%d %z")""": num[-4]})

        if """Time.strptime("20010203 UTC", "%Y%m%d %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("20010203 UTC", "%Y%m%d %z")""": num[-4]})

        if """Time.strptime("2018-365", "%Y-%j")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("2018-365", "%Y-%j")""": num[-4]})

        if """Time.strptime("2018-091", "%Y-%j")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("2018-091", "%Y-%j")""": num[-4]})

    data.get("default").get("ruby").update(data_ruby)


"""clearlinux openjdk test log analysis"""

def Clr_Log_ruby(lines):
    influs_list = ["app_answer", "app_aobench", "app_erb", "app_factorial",
                   "app_fib", "app_lc_fizzbuzz", "app_mandelbrot", "app_pentomino",
                   "app_raise", "app_strconcat", "app_tak", "app_tarai", "app_uri",
                   "array_sample_100k_10", "array_sample_100k_11", "array_sample_100k__100",
                   "array_sample_100k__1k", "array_sample_100k__6k", "array_sample_100k___10k",
                   "array_sample_100k___50k", "array_shift", "array_small_and", "array_small_diff",
                   "array_small_or", "array_sort_block", "array_sort_float", "array_values_at_int",
                   "array_values_at_range", "bighash", "complex_float_add", "complex_float_div",
                   "complex_float_mul", "complex_float_new", "complex_float_power", "complex_float_sub",
                   "dir_empty_p", "enum_lazy_grep_v_100", "enum_lazy_grep_v_20", "enum_lazy_grep_v_50",
                   "enum_lazy_uniq_100", "enum_lazy_uniq_20", "enum_lazy_uniq_50", "erb_render",
                   "fiber_chain", "file_chmod", "file_rename", "hash_aref_dsym", "hash_aref_dsym_long",
                   "hash_aref_fix", "hash_aref_flo", "hash_aref_miss", "hash_aref_str", "hash_aref_sym",
                   "hash_aref_sym_long", "hash_flatten", "hash_ident_flo", "hash_ident_num", "hash_ident_obj",
                   "hash_ident_str", "hash_ident_sym", "hash_keys", "hash_literal_small2", "hash_literal_small4",
                   "hash_literal_small8", "hash_long", "hash_shift", "hash_shift_u16", "hash_shift_u24",
                   "hash_shift_u32", "hash_small2", "hash_small4", "hash_small8", "hash_to_proc",
                   "hash_values", "int_quo", "io_copy_stream_write", "io_copy_stream_write_socket",
                   "io_file_create", "io_file_read", "io_file_write", "io_nonblock_noex", "io_nonblock_noex2",
                   "io_pipe_rw", "io_select", "io_select2", "io_select3", "loop_for", "loop_generator",
                   "loop_times", "loop_whileloop", "loop_whileloop2", "marshal_dump_flo", "marshal_dump_load_geniv",
                   "marshal_dump_load_time",
                   "Calculating-(1..1_000_000).last(100)",
                   "Calculating-(1..1_000_000).last(1000)",
                   "Calculating-(1..1_000_000).last(10000)",
                   "capitalize-1",
                   "capitalize-10",
                   "capitalize-100",
                   "capitalize-1000",
                   "downcase-1",
                   "downcase-10",
                   "downcase-100",
                   "downcase-1000",
                   "require", "require_thread", "securerandom", "so_ackermann",
                   "so_array", "so_binary_trees", "so_concatenate", "so_count_words", "so_exception", "so_fannkuch",
                   "so_fasta", "so_k_nucleotidepreparing", "so_lists", "so_mandelbrot", "so_matrix",
                   "so_meteor_contest",
                   "so_nbody", "so_nested_loop", "so_nsieve", "so_nsieve_bits", "so_object", "so_partial_sums",
                   "so_pidigits", "so_random", "so_reverse_complementpreparing", "so_sieve", "so_spectralnorm",
                   "string_index", "string_scan_re",
                   "string_scan_str",
                   "to_chars-1",
                   "to_chars-10",
                   "to_chars-100",
                   "to_chars-1000",
                   "swapcase-1",
                   "swapcase-10",
                   "swapcase-100",
                   "swapcase-1000",
                   "upcase-1",
                   "upcase-10",
                   "upcase-100",
                   "upcase-1000",
                   """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""",
                   """Time.strptime("1", "%s")""",
                   """Time.strptime("0 +0100", "%s %z")""",
                   """Time.strptime("0 UTC", "%s %z")""",
                   """Time.strptime("1.5", "%s.%N")""",
                   """Time.strptime("1.000000000001", "%s.%N")""",
                   """Time.strptime("20010203 -0200", "%Y%m%d %z")""",
                   """Time.strptime("20010203 UTC", "%Y%m%d %z")""",
                   """Time.strptime("2018-365", "%Y-%j")""",
                   """Time.strptime("2018-091", "%Y-%j")""",
                   "time_subsec", "vm1_attr_ivar",
                   "vm1_attr_ivar_set",
                   "vm1_block", "vm1_blockparam", "vm1_blockparam_call", "vm1_blockparam_pass",
                   "vm1_blockparam_yield",
                   "vm1_const", "vm1_ensure", "vm1_float_simple", "vm1_gc_short_lived",
                   "vm1_gc_short_with_complex_long",
                   "vm1_gc_short_with_long", "vm1_gc_short_with_symbol", "vm1_gc_wb_ary", "vm1_gc_wb_ary_promoted",
                   "vm1_gc_wb_obj", "vm1_gc_wb_obj_promoted", "vm1_ivar", "vm1_ivar_set", "vm1_length",
                   "vm1_lvar_init",
                   "vm1_lvar_set", "vm1_neq", "vm1_not", "vm1_rescue", "vm1_simplereturn", "vm1_swap", "vm1_yield",
                   "vm2_array", "vm2_bigarray", "vm2_bighash", "vm2_case", "vm2_case_lit", "vm2_defined_method",
                   "vm2_dstr", "vm2_eval", "vm2_fiber_switch", "vm2_freezestring", "vm2_method",
                   "vm2_method_missing",
                   "vm2_method_with_block", "vm2_module_ann_const_set", "vm2_module_const_set", "vm2_mutex",
                   "vm2_newlambda",
                   "vm2_poly_method", "vm2_poly_method_ov", "vm2_poly_singleton", "vm2_proc", "vm2_raise1",
                   "vm2_raise2",
                   "vm2_regexp", "vm2_send", "vm2_string_literal", "vm2_struct_big_aref_hi",
                   "vm2_struct_big_aref_lo",
                   "vm2_struct_big_aset", "vm2_struct_big_href_hi", "vm2_struct_big_href_lo", "vm2_struct_big_hset",
                   "vm2_struct_small_aref", "vm2_struct_small_aset", "vm2_struct_small_href",
                   "vm2_struct_small_hset",
                   "vm2_super", "vm2_unif1", "vm2_zsuper", "vm3_backtrace", "vm3_clearmethodcache", "vm3_gc",
                   "vm3_gc_old_full",
                   "vm3_gc_old_immediate", "vm3_gc_old_lazy", "vm_symbol_block_pass", "vm_thread_alive_check1",
                   "vm_thread_close",
                   "vm_thread_condvar1", "vm_thread_condvar2", "vm_thread_create_join", "vm_thread_mutex1",
                   "vm_thread_mutex2",
                   "vm_thread_mutex3", "vm_thread_pass", "vm_thread_pass_flood", "vm_thread_pipe",
                   "vm_thread_queue",
                   "vm_thread_sized_queue", "vm_thread_sized_queue2", "vm_thread_sized_queue3",
                   "vm_thread_sized_queue4"
                   ]

    data_ruby = {}
    for i in lines[
             lines.index("[ruby] [INFO] Test clear docker image:\n"):
             lines.index("Clr-Ruby-Server\n")]:

        for startwith_item in influs_list:
            # if i.startswith(startwith_item) or i.startswith("\t") and startwith_item in i:
            if i.endswith("s/i)\n") and startwith_item in i:
                num = re.findall("\d+\.?\d* s|ERROR", i)
                data_ruby.update({startwith_item: num[-1][:-1]})

        if "so_reverse_complementpreparing" in i:
            start = lines.index(i)
            so_reverse_complementpreparing = lines[start + 1]
            num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
            data_ruby.update({"so_reverse_complementpreparing": num[-1][:-1]})

        if "so_k_nucleotidepreparing" in i:
            start = lines.index(i)
            so_reverse_complementpreparing = lines[start + 1]
            num = re.findall("\d+\.?\d* s", so_reverse_complementpreparing)
            data_ruby.update({"so_k_nucleotidepreparing": num[-1][:-1]})

        # lines = lines[
        #         lines.index("[ruby] [INFO] Test clear docker image:\n"):
        #         lines.index("Clr-Ruby-Server\n")]

    for item in lines:
        if item.startswith("Warming up --------------------------------------\n"):
            up = lines.index(item)

    for item in lines[up:]:
        if item.startswith("Comparison:\n"):
            down = lines[up:].index(item) + up

    for i in lines[up:down]:

        if "(1..1_000_000).last(100)" in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"(1..1_000_000).last(100)": num[-4]})

        if "(1..1_000_000).last(1000)" in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"(1..1_000_000).last(1000)": num[-4]})

        if "(1..1_000_000).last(10000)" in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"(1..1_000_000).last(10000)": num[-4]})

    for i in lines[down:]:

        if i.startswith("Warming up --------------------------------------\n"):
            capit_start = lines[down:].index(i) + down

    for i in lines[capit_start:]:

        if i.startswith("Calculating -------------------------------------\n"):
            calc_start = lines[capit_start:].index(i) + capit_start

    for i in lines[calc_start:]:

        if i.startswith("Comparison:\n"):
            calc_end = lines[calc_start:].index(i) + calc_start

    for i in lines[calc_start:calc_end]:

        if "capitalize-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-1": num[1]})

        if "capitalize-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-10": num[1]})

        if "capitalize-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-100": num[1]})

        if "capitalize-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"capitalize-1000": num[1]})

    for i in lines[calc_end:]:
        if i.startswith("Calculating -------------------------------------\n"):
            downcase_start = lines[calc_end:].index(i) + calc_end

    for i in lines[downcase_start:]:

        if i.startswith("Comparison:\n"):
            downcase_end = lines[downcase_start:].index(i) + downcase_start

    for i in lines[downcase_start:downcase_end]:

        if "downcase-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-1": num[1]})

        if "downcase-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-10": num[1]})

        if "downcase-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-100": num[1]})

        if "downcase-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"downcase-1000": num[1]})

    for i in lines[downcase_end:]:
        if i.startswith("Warming up --------------------------------------\n"):
            to_chars = lines[downcase_end:].index(i) + downcase_end

    for i in lines[to_chars:]:

        if i.startswith("Calculating -------------------------------------\n"):
            to_chars_start = lines[to_chars:].index(i) + to_chars

    for i in lines[to_chars_start:]:

        if i.startswith("Comparison:\n"):
            to_chars_end = lines[to_chars_start:].index(i) + to_chars_start

    for i in lines[to_chars_start:to_chars_end]:

        if "to_chars-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-1": num[1]})

        if "to_chars-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-10": num[1]})

        if "to_chars-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-100": num[1]})

        if "to_chars-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"to_chars-1000": num[1]})

    for i in lines[to_chars_end:]:

        if i.startswith("Warming up --------------------------------------\n"):
            swapcase = lines[to_chars_end:].index(i) + to_chars_end

    for i in lines[swapcase:]:

        if i.startswith("Calculating -------------------------------------\n"):
            swapcase_start = lines[swapcase:].index(i) + swapcase

    for i in lines[swapcase_start:]:

        if i.startswith("Comparison:\n"):
            swapcase_end = lines[swapcase_start:].index(i) + swapcase_start

    for i in lines[swapcase_start:swapcase_end]:

        if "swapcase-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-1": num[1]})

        if "swapcase-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-10": num[1]})

        if "swapcase-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-100": num[1]})

        if "swapcase-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"swapcase-1000": num[1]})

    for i in lines[swapcase_end:]:

        if i.startswith("Calculating -------------------------------------\n"):
            upcase_start = lines[swapcase_end:].index(i) + swapcase_end

    for i in lines[upcase_start:]:

        if i.startswith("Comparison:\n"):
            upcase_end = lines[upcase_start:].index(i) + upcase_start

    for i in lines[upcase_start:upcase_end]:

        if "upcase-1  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-1": num[1]})

        if "upcase-10  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-10": num[1]})

        if "upcase-100  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-100": num[1]})

        if "upcase-1000  " in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"upcase-1000": num[1]})

    for i in lines[upcase_end:]:

        if i.startswith("Calculating -------------------------------------\n"):
            time_start = lines[upcase_end:].index(i) + upcase_end

    for i in lines[time_start:]:

        if i.startswith("Comparison:\n"):
            time_end = lines[time_start:].index(i) + time_start

    for i in lines[time_start:time_end]:

        if """Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")""": num[-4]})

        if """Time.strptime("1", "%s")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("1", "%s")""": num[-4]})

        if """Time.strptime("0 +0100", "%s %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("0 +0100", "%s %z")""": num[-4]})

        if """Time.strptime("0 UTC", "%s %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("0 UTC", "%s %z")""": num[-4]})

        if """Time.strptime("1.5", "%s.%N")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("1.5", "%s.%N")""": num[-4]})

        if """Time.strptime("1.000000000001", "%s.%N")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("1.000000000001", "%s.%N")""": num[-4]})

        if """Time.strptime("20010203 -0200", "%Y%m%d %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("20010203 -0200", "%Y%m%d %z")""": num[-4]})

        if """Time.strptime("20010203 UTC", "%Y%m%d %z")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("20010203 UTC", "%Y%m%d %z")""": num[-4]})

        if """Time.strptime("2018-365", "%Y-%j")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("2018-365", "%Y-%j")""": num[-4]})

        if """Time.strptime("2018-091", "%Y-%j")  """ in i:
            num = re.findall("\d+\.?\d*", i)
            data_ruby.update({"""Time.strptime("2018-091", "%Y-%j")""": num[-4]})

    data.get("clear").get("ruby").update(data_ruby)


def main():
    file_name = r"C:\Users\xinhuizx\Intel-Test-MQservice\2019-07-20-AWS\test_log\openjdk\2019-07-20-01_08_52.log"
    test = read_logs(file_name)

    # status_log = r""
    # status = read_status_logs()

    Log_openjdk(test)
    # Log_postgres(test)
    # Log_ruby(test)
    # Clr_Log_ruby(test)

    # with open('data_New.json', 'w')as f:
    #     json.dump(data, f)

if __name__ == '__main__':
    main()
    pprint(data)
