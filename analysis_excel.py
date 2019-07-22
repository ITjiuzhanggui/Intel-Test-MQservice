import os
import pandas as pd

pd.set_option("expand_frame_repr", False)


# def read_log(file_name):
#     with open(file_name, "r", encoding="utf-8")as f:
#         return f.read()

# def read_status_logs(status_log):
#     with open(status_log, "r", encoding="utf-8")as f:
#         return f.read()


def read_status_log(service_name, writer):
    status_json_filename = r"C:\Users\xinhuizx\Intel-Test-MQservice\2019-07-20-AWS\json\status\1563686517.json"
    df_json = pd.read_json(status_json_filename)
    status_def_dict = df_json.loc[service_name].loc["status_def"]
    status_clr_dict = df_json.loc[service_name].loc["status_Clr"]
    version_ID = status_clr_dict["VERSION_ID"]
    clearlinux_version = df_json.loc["clearlinux_version"].loc["status_Clr"]

    x_status = ["Total", "Base_Layer", "MicroService_layer"]
    status_col = pd.Series(x_status)

    default_total = status_def_dict.get("Total")
    default_base_layer = status_def_dict.get("Base_Layer")
    default_microService_layer = status_def_dict.get("MicroService_layer")
    status_def_list = [default_total, default_base_layer, default_microService_layer]
    status_def_col = pd.Series(status_def_list)

    clear_total = status_clr_dict.get("Total")
    clear_base_layer = status_clr_dict.get("Base_Layer")
    clear_microService_layer = status_clr_dict.get("MicroService_layer")

    status_clr_list = [clear_total, clear_base_layer, clear_microService_layer]
    status_clr_col = pd.Series(status_clr_list)

    data_frame_status = {"Performance": status_col,
                         "Default docker": status_def_col,
                         "clear docker": status_clr_col,
                         "VERSION_ID": version_ID,
                         "clearl_linux_version": clearlinux_version}

    df_exce_status = pd.DataFrame(data_frame_status)
    df_exce_status.to_excel(writer, sheet_name=service_name, index=False, startrow=0)

    print("Successfully status!!!")


def Httpd(writer, df_json, loop_count):
    read_status_log("httpd", writer)
    default_dict = df_json.loc["httpd"].loc["default"]
    clear_dict = df_json.loc["httpd"].loc["clear"]

    x_test = ["Time taken for tests",
              "Time per request",
              "Time per request(all)",
              "Requests per second",
              "Transfer rate"]

    test_col = pd.Series(x_test)

    default_httpd_list = [default_dict["Time taken for tests"],
                          default_dict["Time per request"],
                          default_dict["Time per request(all)"],
                          default_dict["Requests per second"],
                          default_dict["Transfer rate"]
                          ]

    default_col = pd.Series(default_httpd_list)

    clear_httpd_list = [clear_dict["Time taken for tests"],
                        clear_dict["Time per request"],
                        clear_dict["Time per request(all)"],
                        clear_dict["Requests per second"],
                        clear_dict["Transfer rate"]
                        ]

    clear_col = pd.Series(clear_httpd_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col, "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="httpd", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Httpd!!!" % (loop_count + int(1)))


def Nginx(writer, df_json, loop_count):
    read_status_log("nginx", writer)
    default_dict = df_json.loc["nginx"].loc["default"]
    clear_dict = df_json.loc["nginx"].loc["clear"]

    x_test = ["Time taken for tests",
              "Time per request",
              "Time per request(all)",
              "Requests per second",
              "Transfer rate"]

    test_col = pd.Series(x_test)

    default_nginx_list = [default_dict["Time taken for tests"],
                          default_dict["Time per request"],
                          default_dict["Time per request(all)"],
                          default_dict["Requests per second"],
                          default_dict["Transfer rate"]
                          ]

    default_col = pd.Series(default_nginx_list)

    clear_nginx_list = [clear_dict["Time taken for tests"],
                        clear_dict["Time per request"],
                        clear_dict["Time per request(all)"],
                        clear_dict["Requests per second"],
                        clear_dict["Transfer rate"]
                        ]

    clear_col = pd.Series(clear_nginx_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col, "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="nginx", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Nginx!!!" % (loop_count + int(1)))


def Memcached(writer, df_json, loop_count):
    read_status_log("memcached", writer)
    default_dict = df_json.loc["memcached"].loc["default"]
    clear_dict = df_json.loc["memcached"].loc["clear"]

    x_test = ["Sets - Latency",
              "Sets - KB/sec",
              "Gets - Latency",
              "Gets - KB/sec",
              "Total - Latency",
              "Total - KB/sec"]

    test_col = pd.Series(x_test)
    set_values = default_dict["Sets"]
    get_values = default_dict["Gets"]
    total_values = default_dict["Totals"]
    default_memcached_list = [set_values[0].split(":")[-1],
                              set_values[1].split()[0],
                              get_values[0].split(":")[-1],
                              get_values[1].split()[0],
                              total_values[0].split(":")[-1],
                              total_values[1].split()[0]
                              ]

    default_col = pd.Series(default_memcached_list)

    set_values = clear_dict["Sets"]
    get_values = clear_dict["Gets"]
    total_values = clear_dict["Totals"]
    clear_memcached_list = [set_values[0].split(":")[-1],
                            set_values[1].split()[0],
                            get_values[0].split(":")[-1],
                            get_values[1].split()[0],
                            total_values[0].split(":")[-1],
                            total_values[1].split()[0]
                            ]

    clear_col = pd.Series(clear_memcached_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="memcached", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Memcached!!!" % (loop_count + int(1)))


def Redis(writer, df_json, loop_count):
    read_status_log("redis", writer)
    default_dict = df_json.loc["redis"].loc["default"]
    clear_dict = df_json.loc["redis"].loc["clear"]

    x_test = ["PING_INLINE",
              "PING_BULK",
              "SET",
              "GET",
              "INCR",
              "LPUSH",
              "RPUSH",
              "LPOP",
              "RPOP",
              "SADD",
              "HSET",
              "SPOP",
              "LPUSH (needed to benchmark LRANGE)",
              "LRANGE_100 (first 100 elements)",
              "LRANGE_300 (first 300 elements)",
              "LRANGE_500 (first 450 elements)",
              "LRANGE_600 (first 600 elements)",
              "MSET (10 keys)",
              "Sets-Latency",
              "Sets-KB/sec",
              "Gets-Latency",
              "Gets-KB/sec",
              "Totals-Latency",
              "Totals-KB/sec"
              ]

    test_col = pd.Series(x_test)

    default_redis_list = [default_dict["PING_INLINE"],
                          default_dict["PING_BULK"],
                          default_dict["SET"],
                          default_dict["GET"],
                          default_dict["INCR"],
                          default_dict["LPUSH"],
                          default_dict["RPUSH"],
                          default_dict["LPOP"],
                          default_dict["RPOP"],
                          default_dict["SADD"],
                          default_dict["HSET"],
                          default_dict["SPOP"],
                          default_dict["LPUSH (needed to benchmark LRANGE)"],
                          default_dict["LRANGE_100 (first 100 elements)"],
                          default_dict["LRANGE_300 (first 300 elements)"],
                          default_dict["LRANGE_500 (first 450 elements)"],
                          default_dict["LRANGE_600 (first 600 elements)"],
                          default_dict["MSET (10 keys)"],
                          default_dict["Sets-Latency"],
                          default_dict["Sets-KB/sec"],
                          default_dict["Gets-Latency"],
                          default_dict["Gets-KB/sec"],
                          default_dict["Totals-Latency"],
                          default_dict["Totals-KB/sec"]
                          ]

    default_col = pd.Series(default_redis_list)

    clear_redis_list = [clear_dict["PING_INLINE"],
                        clear_dict["PING_BULK"],
                        clear_dict["SET"],
                        clear_dict["GET"],
                        clear_dict["INCR"],
                        clear_dict["LPUSH"],
                        clear_dict["RPUSH"],
                        clear_dict["LPOP"],
                        clear_dict["RPOP"],
                        clear_dict["SADD"],
                        clear_dict["HSET"],
                        clear_dict["SPOP"],
                        clear_dict["LPUSH (needed to benchmark LRANGE)"],
                        clear_dict["LRANGE_100 (first 100 elements)"],
                        clear_dict["LRANGE_300 (first 300 elements)"],
                        clear_dict["LRANGE_500 (first 450 elements)"],
                        clear_dict["LRANGE_600 (first 600 elements)"],
                        clear_dict["MSET (10 keys)"],
                        clear_dict["Sets-Latency"],
                        clear_dict["Sets-KB/sec"],
                        clear_dict["Gets-Latency"],
                        clear_dict["Gets-KB/sec"],
                        clear_dict["Totals-Latency"],
                        clear_dict["Totals-KB/sec"]
                        ]

    clear_col = pd.Series(clear_redis_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="redis", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Redis!!!" % (loop_count + int(1)))


def Php(writer, df_json, loop_count):
    read_status_log("php", writer)
    default_dict = df_json.loc["php"].loc["default"]
    clear_dict = df_json.loc["php"].loc["clear"]

    x_test = ["Score"]

    test_col = pd.Series(x_test)

    default_php_list = default_dict.get("Score")

    default_col = pd.Series(default_php_list)

    clear_php_list = clear_dict.get("Score")

    clear_col = pd.Series(clear_php_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="php", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Php!!!" % (loop_count + int(1)))


def Python(writer, df_json, loop_count):
    read_status_log("python", writer)
    default_dict = df_json.loc["python"].loc["default"]
    clear_dict = df_json.loc["python"].loc["clear"]

    x_test = ["minimum", "average"]
    test_col = pd.Series(x_test)

    # default
    default_minimum_value = default_dict["Totals"][0].get("minimum")
    default_avg_value = default_dict["Totals"][1].get("average")
    default_python_list = [default_minimum_value, default_avg_value]
    default_col = pd.Series(default_python_list)
    # clear
    clear_minimum_value = clear_dict["Totals"][0].get("minimum")
    clear_avg_value = clear_dict["Totals"][1].get("average")
    clear_httpd_list = [clear_minimum_value, clear_avg_value]
    clear_col = pd.Series(clear_httpd_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="python", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Python!!!" % (loop_count + int(1)))


def Node(writer, df_json, loop_count):
    read_status_log("node", writer)
    default_dict = df_json.loc["node"].loc["default"]
    clear_dict = df_json.loc["node"].loc["clear"]

    x_test = ["benchmark-node-octane"]

    test_col = pd.Series(x_test)

    default_node_list = [default_dict["benchmark-node-octane"], ]

    default_col = pd.Series(default_node_list)

    clear_node_list = [clear_dict["benchmark-node-octane"], ]

    clear_col = pd.Series(clear_node_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="node", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Node!!!" % (loop_count + int(1)))


def Golang(writer, df_json, loop_count):
    read_status_log("golang", writer)
    default_dict = df_json.loc["golang"].loc["default"]
    clear_dict = df_json.loc["golang"].loc["clear"]

    x_test = ["BenchmarkBuild",
              "BenchmarkGarbage",
              "BenchmarkHTTP",
              "BenchmarkJSON", ]

    test_col = pd.Series(x_test)

    default_golang_list = [default_dict["BenchmarkBuild"],
                           default_dict["BenchmarkGarbage"],
                           default_dict["BenchmarkHTTP"],
                           default_dict["BenchmarkJSON"]]

    default_col = pd.Series(default_golang_list)

    clear_golang_list = [clear_dict["BenchmarkBuild"],
                         clear_dict["BenchmarkGarbage"],
                         clear_dict["BenchmarkHTTP"],
                         clear_dict["BenchmarkJSON"], ]

    clear_col = pd.Series(clear_golang_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="golang", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Golang!!!" % (loop_count + int(1)))


def Postgres(writer, df_json, loop_count):
    read_status_log("postgres", writer)
    default_dict = df_json.loc["postgres"].loc["default"]
    clear_dict = df_json.loc["postgres"].loc["clear"]

    x_test = ["BUFFER_TEST&SINGLE_THREAD&READ_WRITE",
              "BUFFER_TEST&SINGLE_THREAD&READ_ONLY",
              "BUFFER_TEST&NORMAL_LOAD&READ_WRITE",
              "BUFFER_TEST&NORMAL_LOAD&READ_ONLY",
              "BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE",
              "BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY"
              ]

    test_col = pd.Series(x_test)

    default_postgres_list = [
        default_dict["BUFFER_TEST&SINGLE_THREAD&READ_WRITE"],
        default_dict["BUFFER_TEST&SINGLE_THREAD&READ_ONLY"],
        default_dict["BUFFER_TEST&NORMAL_LOAD&READ_WRITE"],
        default_dict["BUFFER_TEST&NORMAL_LOAD&READ_ONLY"],
        default_dict["BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE"],
        default_dict["BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY"]
    ]

    default_col = pd.Series(default_postgres_list)

    clear_postgres_list = [
        clear_dict["BUFFER_TEST&SINGLE_THREAD&READ_WRITE"],
        clear_dict["BUFFER_TEST&SINGLE_THREAD&READ_ONLY"],
        clear_dict["BUFFER_TEST&NORMAL_LOAD&READ_WRITE"],
        clear_dict["BUFFER_TEST&NORMAL_LOAD&READ_ONLY"],
        clear_dict["BUFFER_TEST&HEAVY_CONNECTION&READ_WRITE"],
        clear_dict["BUFFER_TEST&HEAVY_CONNECTION&READ_ONLY"],
    ]

    clear_col = pd.Series(clear_postgres_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="postgres", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Postgres!!!" % (loop_count + int(1)))


def Tensorflow(writer, df_json, loop_count):
    read_status_log("tensorflow", writer)
    default_dict = df_json.loc["tensorflow"].loc["default"]
    clear_dict = df_json.loc["tensorflow"].loc["clear"]

    x_test = ["Total duration"]

    test_col = pd.Series(x_test)

    default_tensorflow_list = [default_dict["Total duration"]]

    default_col = pd.Series(default_tensorflow_list)

    clear_tensorflow_list = [clear_dict["Total duration"]]

    clear_col = pd.Series(clear_tensorflow_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="tensorflow", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Tensorflow!!!" % (loop_count + int(1)))


def Mariadb(writer, df_json, loop_count):
    read_status_log("mariadb", writer)
    default_dict = df_json.loc["mariadb"].loc["default"]
    clear_dict = df_json.loc["mariadb"].loc["clear"]

    x_test = ["Average number of seconds to run all queries",
              "Minimum number of seconds to run all queries",
              "Maximum number of seconds to run all queries"]

    test_col = pd.Series(x_test)

    default_mariadb_list = [
        default_dict["Average number of seconds to run all queries"],
        default_dict["Minimum number of seconds to run all queries"],
        default_dict["Maximum number of seconds to run all queries"]]

    default_col = pd.Series(default_mariadb_list)

    clear_mariadb_list = [
        clear_dict["Average number of seconds to run all queries"],
        clear_dict["Minimum number of seconds to run all queries"],
        clear_dict["Maximum number of seconds to run all queries"]]

    clear_col = pd.Series(clear_mariadb_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="mariadb", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Mariadb!!!" % (loop_count + int(1)))


def Perl(writer, df_json, loop_count):
    read_status_log("perl", writer)
    default_dict = df_json.loc["perl"].loc["default"]
    clear_dict = df_json.loc["perl"].loc["clear"]

    x_test = ["podhtml.b",
              "noprog.b"]

    test_col = pd.Series(x_test)

    default_perl_list = [default_dict["podhtml.b"],
                         default_dict["noprog.b"]]

    default_col = pd.Series(default_perl_list)

    clear_perl_list = [clear_dict["podhtml.b"],
                       clear_dict["noprog.b"]]

    clear_col = pd.Series(clear_perl_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="perl", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Perl!!!" % (loop_count + int(1)))


def Openjdk(writer, df_json, loop_count):
    read_status_log("openjdk", writer)
    default_dict = df_json.loc["openjdk"].loc["default"]
    clear_dict = df_json.loc["openjdk"].loc["clear"]

    x_test = ["MyBenchmark.testMethod.Score",
              "MyBenchmark.testMethod.Error"]

    test_col = pd.Series(x_test)

    default_openjdk_list = [
        default_dict["MyBenchmark.testMethod.Score"],
        default_dict["MyBenchmark.testMethod.Error"]]

    default_col = pd.Series(default_openjdk_list)

    clear_openjdk_list = [
        clear_dict["MyBenchmark.testMethod.Score"],
        clear_dict["MyBenchmark.testMethod.Error"]]

    clear_col = pd.Series(clear_openjdk_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="openjdk", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Openjdk!!!" % (loop_count + int(1)))


def Rabbitmq(writer, df_json, loop_count):
    read_status_log("rabbitmq", writer)
    default_dict = df_json.loc["rabbitmq"].loc["default"]
    clear_dict = df_json.loc["rabbitmq"].loc["clear"]

    x_test = ["sending rate avg",
              "receiving rate avg"]

    test_col = pd.Series(x_test)

    default_tensorflow_list = [default_dict["sending rate avg"],
                               default_dict["receiving rate avg"]]

    default_col = pd.Series(default_tensorflow_list)

    clear_tensorflow_list = [clear_dict["sending rate avg"],
                             clear_dict["receiving rate avg"]]

    clear_col = pd.Series(clear_tensorflow_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="rabbitmq", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Rabbitmq!!!" % (loop_count + int(1)))


def Ruby(writer, df_json, loop_count):
    read_status_log("ruby", writer)
    default_dict = df_json.loc["ruby"].loc["default"]
    clear_dict = df_json.loc["ruby"].loc["clear"]

    x_test = ["app_answer",
              "app_aobench",
              "app_erb",
              "app_factorial",
              "app_fib",
              "app_lc_fizzbuzz",
              "app_mandelbrot",
              "app_pentomino",
              "app_raise",
              "app_strconcat",
              "app_tak",
              "app_tarai",
              "app_uri",
              "array_sample_100k_10",
              "array_sample_100k_11",
              "array_sample_100k__100",
              "array_sample_100k__1k",
              "array_sample_100k__6k",
              "array_sample_100k___10k",
              "array_sample_100k___50k",
              "array_shift",
              "array_small_and",
              "array_small_diff",
              "array_small_or",
              "array_sort_block",
              "array_sort_float",
              "array_values_at_int",
              "array_values_at_range",
              "bighash",
              "complex_float_add",
              "complex_float_div",
              "complex_float_mul",
              "complex_float_new",
              "complex_float_power",
              "complex_float_sub",
              "dir_empty_p",
              "enum_lazy_grep_v_100",
              "enum_lazy_grep_v_20",
              "enum_lazy_grep_v_50",
              "enum_lazy_uniq_100",
              "enum_lazy_uniq_20",
              "enum_lazy_uniq_50",
              "erb_render",
              "fiber_chain",
              "file_chmod",
              "file_rename",
              "hash_aref_dsym",
              "hash_aref_dsym_long",
              "hash_aref_fix",
              "hash_aref_flo",
              "hash_aref_miss",
              "hash_aref_str",
              "hash_aref_sym",
              "hash_aref_sym_long",
              "hash_flatten",
              "hash_ident_flo",
              "hash_ident_num",
              "hash_ident_obj",
              "hash_ident_str",
              "hash_ident_sym",
              "hash_keys",
              "hash_literal_small2",
              "hash_literal_small4",
              "hash_literal_small8",
              "hash_long",
              "hash_shift",
              "hash_shift_u16",
              "hash_shift_u24",
              "hash_shift_u32",
              "hash_small2",
              "hash_small4",
              "hash_small8",
              "hash_to_proc",
              "hash_values",
              "int_quo",
              "io_copy_stream_write",
              "io_copy_stream_write_socket",
              "io_file_create",
              "io_file_read",
              "io_file_write",
              "io_nonblock_noex",
              "io_nonblock_noex2",
              "io_pipe_rw",
              "io_select",
              "io_select2",
              "io_select3",
              "loop_for",
              "loop_generator",
              "loop_times",
              "loop_whileloop",
              "loop_whileloop2",
              "marshal_dump_flo",
              "marshal_dump_load_geniv",
              "marshal_dump_load_time",
              "(1..1_000_000).last(100)",
              "(1..1_000_000).last(1000)",
              "(1..1_000_000).last(10000)",
              "require",
              "require_thread",
              "securerandom",
              "so_ackermann",
              "so_array",
              "so_binary_trees",
              "so_concatenate",
              "so_count_words",
              "so_exception",
              "so_fannkuch",
              "so_fasta",
              "so_k_nucleotidepreparing",
              "so_lists",
              "so_mandelbrot",
              "so_matrix",
              "so_meteor_contest",
              "so_nbody",
              "so_nested_loop",
              "so_nsieve",
              "so_nsieve_bits",
              "so_object",
              "so_partial_sums",
              "so_pidigits",
              "so_random",
              "so_reverse_complementpreparing",
              "so_sieve",
              "so_spectralnorm",
              "capitalize-1",
              "capitalize-10",
              "capitalize-100",
              "capitalize-1000",
              "downcase-1",
              "downcase-10",
              "downcase-100",
              "downcase-1000",
              "string_index",
              "string_scan_re",
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
              "time_subsec",
              "vm1_attr_ivar",
              "vm1_attr_ivar_set",
              "vm1_block",
              "vm1_blockparam",
              "vm1_blockparam_call",
              "vm1_blockparam_pass",
              "vm1_blockparam_yield",
              "vm1_const",
              "vm1_ensure",
              "vm1_float_simple",
              "vm1_gc_short_lived",
              "vm1_gc_short_with_complex_long",
              "vm1_gc_short_with_long",
              "vm1_gc_short_with_symbol",
              "vm1_gc_wb_ary",
              "vm1_gc_wb_ary_promoted",
              "vm1_gc_wb_obj",
              "vm1_gc_wb_obj_promoted",
              "vm1_ivar",
              "vm1_ivar_set",
              "vm1_length",
              "vm1_lvar_init",
              "vm1_lvar_set",
              "vm1_neq",
              "vm1_not",
              "vm1_rescue",
              "vm1_simplereturn",
              "vm1_swap",
              "vm1_yield",
              "vm2_array",
              "vm2_bigarray",
              "vm2_bighash",
              "vm2_case",
              "vm2_case_lit",
              "vm2_defined_method",
              "vm2_dstr",
              "vm2_eval",
              "vm2_fiber_switch",
              "vm2_freezestring",
              "vm2_method",
              "vm2_method_missing",
              "vm2_method_with_block",
              "vm2_module_ann_const_set",
              "vm2_module_const_set",
              "vm2_mutex",
              "vm2_newlambda",
              "vm2_poly_method",
              "vm2_poly_method_ov",
              "vm2_poly_singleton",
              "vm2_proc",
              "vm2_raise1",
              "vm2_raise2",
              "vm2_regexp",
              "vm2_send",
              "vm2_string_literal",
              "vm2_struct_big_aref_hi",
              "vm2_struct_big_aref_lo",
              "vm2_struct_big_aset",
              "vm2_struct_big_href_hi",
              "vm2_struct_big_href_lo",
              "vm2_struct_big_hset",
              "vm2_struct_small_aref",
              "vm2_struct_small_aset",
              "vm2_struct_small_href",
              "vm2_struct_small_hset",
              "vm2_super",
              "vm2_unif1",
              "vm2_zsuper",
              "vm3_backtrace",
              "vm3_clearmethodcache",
              "vm3_gc",
              "vm3_gc_old_full",
              "vm3_gc_old_immediate",
              "vm3_gc_old_lazy",
              "vm_symbol_block_pass",
              "vm_thread_alive_check1",
              "vm_thread_close",
              "vm_thread_condvar1",
              "vm_thread_condvar2",
              "vm_thread_create_join",
              "vm_thread_mutex1",
              "vm_thread_mutex2",
              "vm_thread_mutex3",
              "vm_thread_pass",
              "vm_thread_pass_flood",
              "vm_thread_pipe",
              "vm_thread_queue",
              "vm_thread_sized_queue",
              "vm_thread_sized_queue2",
              "vm_thread_sized_queue3",
              "vm_thread_sized_queue4"

              ]

    test_col = pd.Series(x_test)

    default_ruby_list = [default_dict["app_answer"],
                         default_dict["app_aobench"],
                         default_dict["app_erb"],
                         default_dict["app_factorial"],
                         default_dict["app_fib"],
                         default_dict["app_lc_fizzbuzz"],
                         default_dict["app_mandelbrot"],
                         default_dict["app_pentomino"],
                         default_dict["app_raise"],
                         default_dict["app_strconcat"],
                         default_dict["app_tak"],
                         default_dict["app_tarai"],
                         default_dict["app_uri"],
                         default_dict["array_sample_100k_10"],
                         default_dict["array_sample_100k_11"],
                         default_dict["array_sample_100k__100"],
                         default_dict["array_sample_100k__1k"],
                         default_dict["array_sample_100k__6k"],
                         default_dict["array_sample_100k___10k"],
                         default_dict["array_sample_100k___50k"],
                         default_dict["array_shift"],
                         default_dict["array_small_and"],
                         default_dict["array_small_diff"],
                         default_dict["array_small_or"],
                         default_dict["array_sort_block"],
                         default_dict["array_sort_float"],
                         default_dict["array_values_at_int"],
                         default_dict["array_values_at_range"],
                         default_dict["bighash"],
                         default_dict["complex_float_add"],
                         default_dict["complex_float_div"],
                         default_dict["complex_float_mul"],
                         default_dict["complex_float_new"],
                         default_dict["complex_float_power"],
                         default_dict["complex_float_sub"],
                         default_dict["dir_empty_p"],
                         default_dict["enum_lazy_grep_v_100"],
                         default_dict["enum_lazy_grep_v_20"],
                         default_dict["enum_lazy_grep_v_50"],
                         default_dict["enum_lazy_uniq_100"],
                         default_dict["enum_lazy_uniq_20"],
                         default_dict["enum_lazy_uniq_50"],
                         default_dict["erb_render"],
                         default_dict["fiber_chain"],
                         default_dict["file_chmod"],
                         default_dict["file_rename"],
                         default_dict["hash_aref_dsym"],
                         default_dict["hash_aref_dsym_long"],
                         default_dict["hash_aref_fix"],
                         default_dict["hash_aref_flo"],
                         default_dict["hash_aref_miss"],
                         default_dict["hash_aref_str"],
                         default_dict["hash_aref_sym"],
                         default_dict["hash_aref_sym_long"],
                         default_dict["hash_flatten"],
                         default_dict["hash_ident_flo"],
                         default_dict["hash_ident_num"],
                         default_dict["hash_ident_obj"],
                         default_dict["hash_ident_str"],
                         default_dict["hash_ident_sym"],
                         default_dict["hash_keys"],
                         default_dict["hash_literal_small2"],
                         default_dict["hash_literal_small4"],
                         default_dict["hash_literal_small8"],
                         default_dict["hash_long"],
                         default_dict["hash_shift"],
                         default_dict["hash_shift_u16"],
                         default_dict["hash_shift_u24"],
                         default_dict["hash_shift_u32"],
                         default_dict["hash_small2"],
                         default_dict["hash_small4"],
                         default_dict["hash_small8"],
                         default_dict["hash_to_proc"],
                         default_dict["hash_values"],
                         default_dict["int_quo"],
                         default_dict["io_copy_stream_write"],
                         default_dict["io_copy_stream_write_socket"],
                         default_dict["io_file_create"],
                         default_dict["io_file_read"],
                         default_dict["io_file_write"],
                         default_dict["io_nonblock_noex"],
                         default_dict["io_nonblock_noex2"],
                         default_dict["io_pipe_rw"],
                         default_dict["io_select"],
                         default_dict["io_select2"],
                         default_dict["io_select3"],
                         default_dict["loop_for"],
                         default_dict["loop_generator"],
                         default_dict["loop_times"],
                         default_dict["loop_whileloop"],
                         default_dict["loop_whileloop2"],
                         default_dict["marshal_dump_flo"],
                         default_dict["marshal_dump_load_geniv"],
                         default_dict["marshal_dump_load_time"],
                         default_dict["(1..1_000_000).last(100)"],
                         default_dict["(1..1_000_000).last(1000)"],
                         default_dict["(1..1_000_000).last(10000)"],
                         default_dict["require"],
                         default_dict["require_thread"],
                         default_dict["securerandom"],
                         default_dict["so_ackermann"],
                         default_dict["so_array"],
                         default_dict["so_binary_trees"],
                         default_dict["so_concatenate"],
                         default_dict["so_count_words"],
                         default_dict["so_exception"],
                         default_dict["so_fannkuch"],
                         default_dict["so_fasta"],
                         default_dict["so_k_nucleotidepreparing"],
                         default_dict["so_lists"],
                         default_dict["so_mandelbrot"],
                         default_dict["so_matrix"],
                         default_dict["so_meteor_contest"],
                         default_dict["so_nbody"],
                         default_dict["so_nested_loop"],
                         default_dict["so_nsieve"],
                         default_dict["so_nsieve_bits"],
                         default_dict["so_object"],
                         default_dict["so_partial_sums"],
                         default_dict["so_pidigits"],
                         default_dict["so_random"],
                         default_dict["so_reverse_complementpreparing"],
                         default_dict["so_sieve"],
                         default_dict["so_spectralnorm"],
                         default_dict["capitalize-1"],
                         default_dict["capitalize-10"],
                         default_dict["capitalize-100"],
                         default_dict["capitalize-1000"],
                         default_dict["downcase-1"],
                         default_dict["downcase-10"],
                         default_dict["downcase-100"],
                         default_dict["downcase-1000"],
                         default_dict["string_index"],
                         default_dict["string_scan_re"],
                         default_dict["string_scan_str"],
                         default_dict["to_chars-1"],
                         default_dict["to_chars-10"],
                         default_dict["to_chars-100"],
                         default_dict["to_chars-1000"],
                         default_dict["swapcase-1"],
                         default_dict["swapcase-10"],
                         default_dict["swapcase-100"],
                         default_dict["swapcase-1000"],
                         default_dict["upcase-1"],
                         default_dict["upcase-10"],
                         default_dict["upcase-100"],
                         default_dict["upcase-1000"],
                         default_dict["""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")"""],
                         default_dict["""Time.strptime("1", "%s")"""],
                         default_dict["""Time.strptime("0 +0100", "%s %z")"""],
                         default_dict["""Time.strptime("0 UTC", "%s %z")"""],
                         default_dict["""Time.strptime("1.5", "%s.%N")"""],
                         default_dict["""Time.strptime("1.000000000001", "%s.%N")"""],
                         default_dict["""Time.strptime("20010203 -0200", "%Y%m%d %z")"""],
                         default_dict["""Time.strptime("20010203 UTC", "%Y%m%d %z")"""],
                         default_dict["""Time.strptime("2018-365", "%Y-%j")"""],
                         default_dict["""Time.strptime("2018-091", "%Y-%j")"""],
                         default_dict["time_subsec"],
                         default_dict["vm1_attr_ivar"],
                         default_dict["vm1_attr_ivar_set"],
                         default_dict["vm1_block"],
                         default_dict["vm1_blockparam"],
                         default_dict["vm1_blockparam_call"],
                         default_dict["vm1_blockparam_pass"],
                         default_dict["vm1_blockparam_yield"],
                         default_dict["vm1_const"],
                         default_dict["vm1_ensure"],
                         default_dict["vm1_float_simple"],
                         default_dict["vm1_gc_short_lived"],
                         default_dict["vm1_gc_short_with_complex_long"],
                         default_dict["vm1_gc_short_with_long"],
                         default_dict["vm1_gc_short_with_symbol"],
                         default_dict["vm1_gc_wb_ary"],
                         default_dict["vm1_gc_wb_ary_promoted"],
                         default_dict["vm1_gc_wb_obj"],
                         default_dict["vm1_gc_wb_obj_promoted"],
                         default_dict["vm1_ivar"],
                         default_dict["vm1_ivar_set"],
                         default_dict["vm1_length"],
                         default_dict["vm1_lvar_init"],
                         default_dict["vm1_lvar_set"],
                         default_dict["vm1_neq"],
                         default_dict["vm1_not"],
                         default_dict["vm1_rescue"],
                         default_dict["vm1_simplereturn"],
                         default_dict["vm1_swap"],
                         default_dict["vm1_yield"],
                         default_dict["vm2_array"],
                         default_dict["vm2_bigarray"],
                         default_dict["vm2_bighash"],
                         default_dict["vm2_case"],
                         default_dict["vm2_case_lit"],
                         default_dict["vm2_defined_method"],
                         default_dict["vm2_dstr"],
                         default_dict["vm2_eval"],
                         default_dict["vm2_fiber_switch"],
                         default_dict["vm2_freezestring"],
                         default_dict["vm2_method"],
                         default_dict["vm2_method_missing"],
                         default_dict["vm2_method_with_block"],
                         default_dict["vm2_module_ann_const_set"],
                         default_dict["vm2_module_const_set"],
                         default_dict["vm2_mutex"],
                         default_dict["vm2_newlambda"],
                         default_dict["vm2_poly_method"],
                         default_dict["vm2_poly_method_ov"],
                         default_dict["vm2_poly_singleton"],
                         default_dict["vm2_proc"],
                         default_dict["vm2_raise1"],
                         default_dict["vm2_raise2"],
                         default_dict["vm2_regexp"],
                         default_dict["vm2_send"],
                         default_dict["vm2_string_literal"],
                         default_dict["vm2_struct_big_aref_hi"],
                         default_dict["vm2_struct_big_aref_lo"],
                         default_dict["vm2_struct_big_aset"],
                         default_dict["vm2_struct_big_href_hi"],
                         default_dict["vm2_struct_big_href_lo"],
                         default_dict["vm2_struct_big_hset"],
                         default_dict["vm2_struct_small_aref"],
                         default_dict["vm2_struct_small_aset"],
                         default_dict["vm2_struct_small_href"],
                         default_dict["vm2_struct_small_hset"],
                         default_dict["vm2_super"],
                         default_dict["vm2_unif1"],
                         default_dict["vm2_zsuper"],
                         default_dict["vm3_backtrace"],
                         default_dict["vm3_clearmethodcache"],
                         default_dict["vm3_gc"],
                         default_dict["vm3_gc_old_full"],
                         default_dict["vm3_gc_old_immediate"],
                         default_dict["vm3_gc_old_lazy"],
                         default_dict["vm_symbol_block_pass"],
                         default_dict["vm_thread_alive_check1"],
                         default_dict["vm_thread_close"],
                         default_dict["vm_thread_condvar1"],
                         default_dict["vm_thread_condvar2"],
                         default_dict["vm_thread_create_join"],
                         default_dict["vm_thread_mutex1"],
                         default_dict["vm_thread_mutex2"],
                         default_dict["vm_thread_mutex3"],
                         default_dict["vm_thread_pass"],
                         default_dict["vm_thread_pass_flood"],
                         default_dict["vm_thread_pipe"],
                         default_dict["vm_thread_queue"],
                         default_dict["vm_thread_sized_queue"],
                         default_dict["vm_thread_sized_queue2"],
                         default_dict["vm_thread_sized_queue3"],
                         default_dict["vm_thread_sized_queue4"]
                         ]

    default_col = pd.Series(default_ruby_list)

    clear_ruby_list = [clear_dict["app_answer"],
                       clear_dict["app_aobench"],
                       clear_dict["app_erb"],
                       clear_dict["app_factorial"],
                       clear_dict["app_fib"],
                       clear_dict["app_lc_fizzbuzz"],
                       clear_dict["app_mandelbrot"],
                       clear_dict["app_pentomino"],
                       clear_dict["app_raise"],
                       clear_dict["app_strconcat"],
                       clear_dict["app_tak"],
                       clear_dict["app_tarai"],
                       clear_dict["app_uri"],
                       clear_dict["array_sample_100k_10"],
                       clear_dict["array_sample_100k_11"],
                       clear_dict["array_sample_100k__100"],
                       clear_dict["array_sample_100k__1k"],
                       clear_dict["array_sample_100k__6k"],
                       clear_dict["array_sample_100k___10k"],
                       clear_dict["array_sample_100k___50k"],
                       clear_dict["array_shift"],
                       clear_dict["array_small_and"],
                       clear_dict["array_small_diff"],
                       clear_dict["array_small_or"],
                       clear_dict["array_sort_block"],
                       clear_dict["array_sort_float"],
                       clear_dict["array_values_at_int"],
                       clear_dict["array_values_at_range"],
                       clear_dict["bighash"],
                       clear_dict["complex_float_add"],
                       clear_dict["complex_float_div"],
                       clear_dict["complex_float_mul"],
                       clear_dict["complex_float_new"],
                       clear_dict["complex_float_power"],
                       clear_dict["complex_float_sub"],
                       clear_dict["dir_empty_p"],
                       clear_dict["enum_lazy_grep_v_100"],
                       clear_dict["enum_lazy_grep_v_20"],
                       clear_dict["enum_lazy_grep_v_50"],
                       clear_dict["enum_lazy_uniq_100"],
                       clear_dict["enum_lazy_uniq_20"],
                       clear_dict["enum_lazy_uniq_50"],
                       clear_dict["erb_render"],
                       clear_dict["fiber_chain"],
                       clear_dict["file_chmod"],
                       clear_dict["file_rename"],
                       clear_dict["hash_aref_dsym"],
                       clear_dict["hash_aref_dsym_long"],
                       clear_dict["hash_aref_fix"],
                       clear_dict["hash_aref_flo"],
                       clear_dict["hash_aref_miss"],
                       clear_dict["hash_aref_str"],
                       clear_dict["hash_aref_sym"],
                       clear_dict["hash_aref_sym_long"],
                       clear_dict["hash_flatten"],
                       clear_dict["hash_ident_flo"],
                       clear_dict["hash_ident_num"],
                       clear_dict["hash_ident_obj"],
                       clear_dict["hash_ident_str"],
                       clear_dict["hash_ident_sym"],
                       clear_dict["hash_keys"],
                       clear_dict["hash_literal_small2"],
                       clear_dict["hash_literal_small4"],
                       clear_dict["hash_literal_small8"],
                       clear_dict["hash_long"],
                       clear_dict["hash_shift"],
                       clear_dict["hash_shift_u16"],
                       clear_dict["hash_shift_u24"],
                       clear_dict["hash_shift_u32"],
                       clear_dict["hash_small2"],
                       clear_dict["hash_small4"],
                       clear_dict["hash_small8"],
                       clear_dict["hash_to_proc"],
                       clear_dict["hash_values"],
                       clear_dict["int_quo"],
                       clear_dict["io_copy_stream_write"],
                       clear_dict["io_copy_stream_write_socket"],
                       clear_dict["io_file_create"],
                       clear_dict["io_file_read"],
                       clear_dict["io_file_write"],
                       clear_dict["io_nonblock_noex"],
                       clear_dict["io_nonblock_noex2"],
                       clear_dict["io_pipe_rw"],
                       clear_dict["io_select"],
                       clear_dict["io_select2"],
                       clear_dict["io_select3"],
                       clear_dict["loop_for"],
                       clear_dict["loop_generator"],
                       clear_dict["loop_times"],
                       clear_dict["loop_whileloop"],
                       clear_dict["loop_whileloop2"],
                       clear_dict["marshal_dump_flo"],
                       clear_dict["marshal_dump_load_geniv"],
                       clear_dict["marshal_dump_load_time"],
                       clear_dict["(1..1_000_000).last(100)"],
                       clear_dict["(1..1_000_000).last(1000)"],
                       clear_dict["(1..1_000_000).last(10000)"],
                       clear_dict["require"],
                       clear_dict["require_thread"],
                       clear_dict["securerandom"],
                       clear_dict["so_ackermann"],
                       clear_dict["so_array"],
                       clear_dict["so_binary_trees"],
                       clear_dict["so_concatenate"],
                       clear_dict["so_count_words"],
                       clear_dict["so_exception"],
                       clear_dict["so_fannkuch"],
                       clear_dict["so_fasta"],
                       clear_dict["so_k_nucleotidepreparing"],
                       clear_dict["so_lists"],
                       clear_dict["so_mandelbrot"],
                       clear_dict["so_matrix"],
                       clear_dict["so_meteor_contest"],
                       clear_dict["so_nbody"],
                       clear_dict["so_nested_loop"],
                       clear_dict["so_nsieve"],
                       clear_dict["so_nsieve_bits"],
                       clear_dict["so_object"],
                       clear_dict["so_partial_sums"],
                       clear_dict["so_pidigits"],
                       clear_dict["so_random"],
                       clear_dict["so_reverse_complementpreparing"],
                       clear_dict["so_sieve"],
                       clear_dict["so_spectralnorm"],
                       clear_dict["capitalize-1"],
                       clear_dict["capitalize-10"],
                       clear_dict["capitalize-100"],
                       clear_dict["capitalize-1000"],
                       clear_dict["downcase-1"],
                       clear_dict["downcase-10"],
                       clear_dict["downcase-100"],
                       clear_dict["downcase-1000"],
                       clear_dict["string_index"],
                       clear_dict["string_scan_re"],
                       clear_dict["string_scan_str"],
                       clear_dict["to_chars-1"],
                       clear_dict["to_chars-10"],
                       clear_dict["to_chars-100"],
                       clear_dict["to_chars-1000"],
                       clear_dict["swapcase-1"],
                       clear_dict["swapcase-10"],
                       clear_dict["swapcase-100"],
                       clear_dict["swapcase-1000"],
                       clear_dict["upcase-1"],
                       clear_dict["upcase-10"],
                       clear_dict["upcase-100"],
                       clear_dict["upcase-1000"],
                       clear_dict["""Time.strptime("28/Aug/2005:06:54:20 +0000", "%d/%b/%Y:%T %z")"""],
                       clear_dict["""Time.strptime("1", "%s")"""],
                       clear_dict["""Time.strptime("0 +0100", "%s %z")"""],
                       clear_dict["""Time.strptime("0 UTC", "%s %z")"""],
                       clear_dict["""Time.strptime("1.5", "%s.%N")"""],
                       clear_dict["""Time.strptime("1.000000000001", "%s.%N")"""],
                       clear_dict["""Time.strptime("20010203 -0200", "%Y%m%d %z")"""],
                       clear_dict["""Time.strptime("20010203 UTC", "%Y%m%d %z")"""],
                       clear_dict["""Time.strptime("2018-365", "%Y-%j")"""],
                       clear_dict["""Time.strptime("2018-091", "%Y-%j")"""],
                       clear_dict["time_subsec"],
                       clear_dict["vm1_attr_ivar"],
                       clear_dict["vm1_attr_ivar_set"],
                       clear_dict["vm1_block"],
                       clear_dict["vm1_blockparam"],
                       clear_dict["vm1_blockparam_call"],
                       clear_dict["vm1_blockparam_pass"],
                       clear_dict["vm1_blockparam_yield"],
                       clear_dict["vm1_const"],
                       clear_dict["vm1_ensure"],
                       clear_dict["vm1_float_simple"],
                       clear_dict["vm1_gc_short_lived"],
                       clear_dict["vm1_gc_short_with_complex_long"],
                       clear_dict["vm1_gc_short_with_long"],
                       clear_dict["vm1_gc_short_with_symbol"],
                       clear_dict["vm1_gc_wb_ary"],
                       clear_dict["vm1_gc_wb_ary_promoted"],
                       clear_dict["vm1_gc_wb_obj"],
                       clear_dict["vm1_gc_wb_obj_promoted"],
                       clear_dict["vm1_ivar"],
                       clear_dict["vm1_ivar_set"],
                       clear_dict["vm1_length"],
                       clear_dict["vm1_lvar_init"],
                       clear_dict["vm1_lvar_set"],
                       clear_dict["vm1_neq"],
                       clear_dict["vm1_not"],
                       clear_dict["vm1_rescue"],
                       clear_dict["vm1_simplereturn"],
                       clear_dict["vm1_swap"],
                       clear_dict["vm1_yield"],
                       clear_dict["vm2_array"],
                       clear_dict["vm2_bigarray"],
                       clear_dict["vm2_bighash"],
                       clear_dict["vm2_case"],
                       clear_dict["vm2_case_lit"],
                       clear_dict["vm2_defined_method"],
                       clear_dict["vm2_dstr"],
                       clear_dict["vm2_eval"],
                       clear_dict["vm2_fiber_switch"],
                       clear_dict["vm2_freezestring"],
                       clear_dict["vm2_method"],
                       clear_dict["vm2_method_missing"],
                       clear_dict["vm2_method_with_block"],
                       clear_dict["vm2_module_ann_const_set"],
                       clear_dict["vm2_module_const_set"],
                       clear_dict["vm2_mutex"],
                       clear_dict["vm2_newlambda"],
                       clear_dict["vm2_poly_method"],
                       clear_dict["vm2_poly_method_ov"],
                       clear_dict["vm2_poly_singleton"],
                       clear_dict["vm2_proc"],
                       clear_dict["vm2_raise1"],
                       clear_dict["vm2_raise2"],
                       clear_dict["vm2_regexp"],
                       clear_dict["vm2_send"],
                       clear_dict["vm2_string_literal"],
                       clear_dict["vm2_struct_big_aref_hi"],
                       clear_dict["vm2_struct_big_aref_lo"],
                       clear_dict["vm2_struct_big_aset"],
                       clear_dict["vm2_struct_big_href_hi"],
                       clear_dict["vm2_struct_big_href_lo"],
                       clear_dict["vm2_struct_big_hset"],
                       clear_dict["vm2_struct_small_aref"],
                       clear_dict["vm2_struct_small_aset"],
                       clear_dict["vm2_struct_small_href"],
                       clear_dict["vm2_struct_small_hset"],
                       clear_dict["vm2_super"],
                       clear_dict["vm2_unif1"],
                       clear_dict["vm2_zsuper"],
                       clear_dict["vm3_backtrace"],
                       clear_dict["vm3_clearmethodcache"],
                       clear_dict["vm3_gc"],
                       clear_dict["vm3_gc_old_full"],
                       clear_dict["vm3_gc_old_immediate"],
                       clear_dict["vm3_gc_old_lazy"],
                       clear_dict["vm_symbol_block_pass"],
                       clear_dict["vm_thread_alive_check1"],
                       clear_dict["vm_thread_close"],
                       clear_dict["vm_thread_condvar1"],
                       clear_dict["vm_thread_condvar2"],
                       clear_dict["vm_thread_create_join"],
                       clear_dict["vm_thread_mutex1"],
                       clear_dict["vm_thread_mutex2"],
                       clear_dict["vm_thread_mutex3"],
                       clear_dict["vm_thread_pass"],
                       clear_dict["vm_thread_pass_flood"],
                       clear_dict["vm_thread_pipe"],
                       clear_dict["vm_thread_queue"],
                       clear_dict["vm_thread_sized_queue"],
                       clear_dict["vm_thread_sized_queue2"],
                       clear_dict["vm_thread_sized_queue3"],
                       clear_dict["vm_thread_sized_queue4"]
                       ]

    clear_col = pd.Series(clear_ruby_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col, "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="ruby", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Ruby!!!" % (loop_count + int(1)))


def Flink(writer, df_json, loop_count):
    read_status_log("flink", writer)
    default_dict = df_json.loc["flink"].loc["default"]
    clear_dict = df_json.loc["flink"].loc["clear"]
    
    x_test = ["KeyByBenchmarks.arrayKeyBy",
              "KeyByBenchmarks.tupleKeyBy",
              "MemoryStateBackendBenchmark.stateBackends-FS",
              "MemoryStateBackendBenchmark.stateBackends-FS_ASYNC",
              "MemoryStateBackendBenchmark.stateBackends-MEMORY",
              "RocksStateBackendBenchmark.stateBackends-ROCKS",
              "RocksStateBackendBenchmark.stateBackends-ROCKS_INC",
              "SerializationFrameworkMiniBenchmarks.serializerAvro",
              "SerializationFrameworkMiniBenchmarks.serializerKryo",
              "SerializationFrameworkMiniBenchmarks.serializerPojo",
              "SerializationFrameworkMiniBenchmarks.serializerRow",
              "SerializationFrameworkMiniBenchmarks.serializerTuple",
              "StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1",
              "StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1,100ms",
              "StreamNetworkThroughputBenchmarkExecutor.networkThroughput-100,1ms",
              "StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,100ms",
              "StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,1ms",
              "SumLongsBenchmark.benchmarkCount",
              "WindowBenchmarks.globalWindow",
              "WindowBenchmarks.sessionWindow",
              "WindowBenchmarks.slidingWindow",
              "WindowBenchmarks.tumblingWindow"
             ]

    test_col = pd.Series(x_test)
    
    default_flink_list =[ default_dict["KeyByBenchmarks.arrayKeyBy"],
                          default_dict["KeyByBenchmarks.tupleKeyBy"],
                          default_dict["MemoryStateBackendBenchmark.stateBackends-FS"],
                          default_dict["MemoryStateBackendBenchmark.stateBackends-FS_ASYNC"],
                          default_dict["MemoryStateBackendBenchmark.stateBackends-MEMORY"],
                          default_dict["RocksStateBackendBenchmark.stateBackends-ROCKS"],
                          default_dict["RocksStateBackendBenchmark.stateBackends-ROCKS_INC"],
                          default_dict["SerializationFrameworkMiniBenchmarks.serializerAvro"],
                          default_dict["SerializationFrameworkMiniBenchmarks.serializerKryo"],
                          default_dict["SerializationFrameworkMiniBenchmarks.serializerPojo"],
                          default_dict["SerializationFrameworkMiniBenchmarks.serializerRow"],
                          default_dict["SerializationFrameworkMiniBenchmarks.serializerTuple"],
                          default_dict["StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1"],
                          default_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1,100ms"],
                          default_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-100,1ms"],
                          default_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,100ms"],
                          default_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,1ms"],
                          default_dict["SumLongsBenchmark.benchmarkCount"],
                          default_dict["WindowBenchmarks.globalWindow"],
                          default_dict["WindowBenchmarks.sessionWindow"],
                          default_dict["WindowBenchmarks.slidingWindow"],
                          default_dict["WindowBenchmarks.tumblingWindow"]]

    default_col = pd.Series(default_flink_list)

    clear_flink_list = [clear_dict["KeyByBenchmarks.arrayKeyBy"],
                        clear_dict["KeyByBenchmarks.tupleKeyBy"],
                        clear_dict["MemoryStateBackendBenchmark.stateBackends-FS"],
                        clear_dict["MemoryStateBackendBenchmark.stateBackends-FS_ASYNC"],
                        clear_dict["MemoryStateBackendBenchmark.stateBackends-MEMORY"],
                        clear_dict["RocksStateBackendBenchmark.stateBackends-ROCKS"],
                        clear_dict["RocksStateBackendBenchmark.stateBackends-ROCKS_INC"],
                        clear_dict["SerializationFrameworkMiniBenchmarks.serializerAvro"],
                        clear_dict["SerializationFrameworkMiniBenchmarks.serializerKryo"],
                        clear_dict["SerializationFrameworkMiniBenchmarks.serializerPojo"],
                        clear_dict["SerializationFrameworkMiniBenchmarks.serializerRow"],
                        clear_dict["SerializationFrameworkMiniBenchmarks.serializerTuple"],
                        clear_dict["StreamNetworkLatencyBenchmarkExecutor.networkLatency1to1"],
                        clear_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1,100ms"],
                        clear_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-100,1ms"],
                        clear_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,100ms"],
                        clear_dict["StreamNetworkThroughputBenchmarkExecutor.networkThroughput-1000,1ms"],
                        clear_dict["SumLongsBenchmark.benchmarkCount"],
                        clear_dict["WindowBenchmarks.globalWindow"],
                        clear_dict["WindowBenchmarks.sessionWindow"],
                        clear_dict["WindowBenchmarks.slidingWindow"],
                        clear_dict["WindowBenchmarks.tumblingWindow"]]

    clear_col = pd.Series(clear_flink_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="flink", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully flink!!!" % (loop_count + int(1)))


def Cassandra(writer, df_json, loop_count):
    read_status_log("cassandra", writer)
    default_dict = df_json.loc["cassandra"].loc["default"]
    clear_dict = df_json.loc["cassandra"].loc["clear"]

    x_test = ["cassandra-stress write test - Op rate(op/s)",
              "cassandra-stress write test - Latency mean(ms)",
              "cassandra-stress read test - 4 threads - Op rate(op/s)",
              "cassandra-stress read test - 4 threads - Latency mean(ms)",
              "cassandra-stress read test - 8 threads - Op rate(op/s)",
              "cassandra-stress read test - 8 threads - Latency mean(ms)",
              "cassandra-stress read test - 16 threads - Op rate(op/s)",
              "cassandra-stress read test - 16 threads - Latency mean(ms)",
              "cassandra-stress read test - 24 threads - Op rate(op/s)",
              "cassandra-stress read test - 24 threads - Latency mean(ms)",
              "cassandra-stress read test - 36 threads - Op rate(op/s)",
              "cassandra-stress read test - 36 threads - Latency mean(ms)",
              "cassandra-stress read test - 54 threads - Op rate(op/s)",
              "cassandra-stress read test - 54 threads - Latency mean(ms)"
              ]

    test_col = pd.Series(x_test)

    default_cassandra_list = [
        default_dict["cassandra-stress write test - Op rate(op/s)"],
        default_dict["cassandra-stress write test - Latency mean(ms)"],
        default_dict["cassandra-stress read test - 4 threads - Op rate(op/s)"],
        default_dict["cassandra-stress read test - 4 threads - Latency mean(ms)"],
        default_dict["cassandra-stress read test - 8 threads - Op rate(op/s)"],
        default_dict["cassandra-stress read test - 8 threads - Latency mean(ms)"],
        default_dict["cassandra-stress read test - 16 threads - Op rate(op/s)"],
        default_dict["cassandra-stress read test - 16 threads - Latency mean(ms)"],
        default_dict["cassandra-stress read test - 24 threads - Op rate(op/s)"],
        default_dict["cassandra-stress read test - 24 threads - Latency mean(ms)"],
        default_dict["cassandra-stress read test - 36 threads - Op rate(op/s)"],
        default_dict["cassandra-stress read test - 36 threads - Latency mean(ms)"],
        default_dict["cassandra-stress read test - 54 threads - Op rate(op/s)"],
        default_dict["cassandra-stress read test - 54 threads - Latency mean(ms)"]]


    default_col = pd.Series(default_cassandra_list)

    clear_cassandra_list = [
        clear_dict["cassandra-stress write test - Op rate(op/s)"],
        clear_dict["cassandra-stress write test - Latency mean(ms)"],
        clear_dict["cassandra-stress read test - 4 threads - Op rate(op/s)"],
        clear_dict["cassandra-stress read test - 4 threads - Latency mean(ms)"],
        clear_dict["cassandra-stress read test - 8 threads - Op rate(op/s)"],
        clear_dict["cassandra-stress read test - 8 threads - Latency mean(ms)"],
        clear_dict["cassandra-stress read test - 16 threads - Op rate(op/s)"],
        clear_dict["cassandra-stress read test - 16 threads - Latency mean(ms)"],
        clear_dict["cassandra-stress read test - 24 threads - Op rate(op/s)"],
        clear_dict["cassandra-stress read test - 24 threads - Latency mean(ms)"],
        clear_dict["cassandra-stress read test - 36 threads - Op rate(op/s)"],
        clear_dict["cassandra-stress read test - 36 threads - Latency mean(ms)"],
        clear_dict["cassandra-stress read test - 54 threads - Op rate(op/s)"],
        clear_dict["cassandra-stress read test - 54 threads - Latency mean(ms)"]]

    clear_col = pd.Series(clear_cassandra_list)

    data_frame_test = {"Performance %d" % (loop_count + 1): test_col,
                       "Default docker": default_col,
                       "clear docker": clear_col}

    df_exce_test = pd.DataFrame(data_frame_test)

    df_exce_test.to_excel(writer, sheet_name="cassandra", index=False, startrow=9, startcol=4 * loop_count)

    print("Round %d Save Successfully Cassandra!!!" % (loop_count + int(1)))


def main():
    loop_count = 0

    json_filename = r"C:\Users\xinhuizx\Intel-Test-MQservice\2019-07-20-AWS\json\test"
    xlsx = r"C:\Users\xinhuizx\Intel-Test-MQservice\MQ_tset.xlsx"

    writer = pd.ExcelWriter(xlsx)
    # read_status_log(writer, status_json_filename)

    for root_dir, _, files in os.walk(json_filename):
        for json_filename in files:
            full_file_name = os.path.join(root_dir, json_filename)
            df_json = pd.read_json(full_file_name)
            # df_json = pd.read_json(r"C:\Users\xinhuizx\Intel-Test-MQservice\DATA_TEST.json")

            # Httpd(writer, df_json, loop_count)
            # Nginx(writer, df_json, loop_count)
            # Redis(writer, df_json, loop_count)
            # Memcached(writer, df_json, loop_count)
            # Php(writer, df_json, loop_count)
            # Python(writer, df_json, loop_count)
            # Node(writer, df_json, loop_count)
            # Golang(writer, df_json, loop_count)
            # Postgres(writer, df_json, loop_count)
            # Tensorflow(writer, df_json, loop_count)
            # Mariadb(writer, df_json, loop_count)
            # Perl(writer, df_json, loop_count)
            # Openjdk(writer, df_json, loop_count)
            # Rabbitmq(writer, df_json, loop_count)
            # Ruby(writer, df_json, loop_count)
            # Flink(writer, df_json, loop_count)
            Cassandra(writer, df_json, loop_count)
            loop_count += 1

    writer.save()


if __name__ == '__main__':
    main()

"""
test_cmd = ["make httpd", "make nginx", "make memcached", "make redis", "make php", "make python", "make node",
            "make golang", "make postgres", "make tensorflow", "make mariadb", "make perl", "make openjdk",
            "make rabbitmq","make ruby"，"make flink"]
"""
"""
test_cmd = ["make postgres", "make openjdk", "make ruby", "make flink", "make cassandra"]

Traceback (most recent call last):
  File "./run_script.py", line 226, in <module>
    status_anlies(num)
  File "./run_script.py", line 92, in status_anlies
    exect_contest(StaDefHttpd().serialization)
  File "/home/auto_latest/core/statusDef.py", line 17, in __init__
    self.data = json.load(f)
  File "/usr/lib/python3.7/json/__init__.py", line 296, in load
    parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)
  File "/usr/lib/python3.7/json/__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "/usr/lib/python3.7/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/lib/python3.7/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 63 column 13 (char 964)


--privileged

--privileged


"""

"""Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running"""
