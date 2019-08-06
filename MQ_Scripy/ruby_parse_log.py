def parse_ruby_log():
    filename = r"C:\Users\xinhuizx\Intel-Test-MQservice\log\2019-07-24\test_log\ruby\2019-07-26-07_55_18.log"
    with open(filename, encoding='utf-8') as f:
        # for line in f.readlines():
        # newlines.append(line.split("\n")[0])
        # newlines.append(line)
        return f.readlines()


def ruby(lines):
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

    line_dict = {}
    for line in ret_lines:
        # print(line)
        line_split = line.split()
        key_str = line_split[0]
        value = line_split[1]
        if "Time" in line:
            time_line_split = line.split("s -")
            time_value = time_line_split[0].split()[-1]
            # print(time_value)
            line_dict.update({line_split[0] + line_split[1]: time_value})
        elif not value.startswith("/"):
            # print(value)
            try:
                key_str = float(str(key_str))
            except Exception:
                pass
            if not isinstance(key_str, float):
                tmp_dict = {key_str: value}
                line_dict.update(tmp_dict)

    for key, value in line_dict.items():
        print(key, ": ", value)
        pass
    print("value len:", len(line_dict.values()))
    print("key len:", len(line_dict.keys()))


if __name__ == '__main__':
    lines = parse_ruby_log()
    ruby(lines)
