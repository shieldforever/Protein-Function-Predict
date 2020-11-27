import os
import csv
import json
import math
import sys

def solve():
    ans_bp_dict = {}
    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            para_w = float(para_w_ / 100.0)
            for para_k in range(10, 45, 5):
                for num_of_neighbor in range(150, 160, 10):
                    for i in range(0, para_k):
                        bp_data_file_path = os.path.join('bp-data', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor) + '-' + str(i) + '.json')
                        file = open(bp_data_file_path, "r")
                        bp_json = json.load(file)
                        bp_data  = bp_json["data"]
                        for i in range(len(bp_data)):
                            go_id = bp_data[i]["go_id"]
                            if ans_bp_dict.__contains__(go_id):
                                ans_bp_dict[go_id] += 1
                            else:
                                ans_bp_dict[go_id] = 1
                        file.close()
    tmp = sorted(ans_bp_dict.items(), key = lambda kv:kv[1], reverse=True)
    length = len(tmp)
    print(length)
    ans_bp_list = []
    for i in range(length):
        ans_bp_list.append(tmp[i][0])
    # print(ans_bp_list)
    file = open("model-bp-go.txt", "w")
    for i in ans_bp_list:
        file.write(i + '\n')
    file.close()

if __name__ == "__main__":

    solve()