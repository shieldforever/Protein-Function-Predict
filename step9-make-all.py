import os
import csv
import json
import math
import sys

test_protein_to_vector_list = []

score_list = []

def cal_distance(list1, list2):
    ans = 0
    length = len(list1)
    for i in range(length):
        delta = (list1[i] - list2[i]) * (list1[i] - list2[i])
        ans += delta
    return math.sqrt(ans)

def score_function(distance, p_value_str):
    a = 0
    b = 0
    c = 0
    # print(p_value_str)
    if p_value_str.find('e') != -1:
        x = p_value_str.split('e')
        a = math.log10(float(x[0]))
        b = int(x[1])
    else:
        if p_value_str == '0':
            a = 0
            b = -308
        else:
            a = math.log10(float(p_value_str))
            b = 0
    
    c = math.exp(-distance)
    score = -(a+b) * c
    return score

def calculate(protein_dict):
    print("calculating:" + protein_dict["protein"])
    vector_list = protein_dict["vector_list"] # it's a dictionary!
    ans_bp_dict = {}
    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            # print(para_w_)
            # print(para_w_ / 100)
            para_w = float(para_w_ / 100.0)
            # print(para_w)
            for para_k in range(10, 45, 5):
                for num_of_neighbor in range(150, 160, 10):
                    for i in range(0, para_k):
                        bp_data_file_path = os.path.join('bp-data', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor) + '-' + str(i) + '.json')
                        file = open(bp_data_file_path, "r")
                        bp_json = json.load(file)
                        bp_vector = bp_json["vector"]
                        bp_data  = bp_json["data"]
                        para = str(para_l) + '-' + str('%.2f' % para_w)
                        distance = cal_distance(bp_vector, vector_list[para])
                        for i in range(len(bp_data)):
                            go_id = bp_data[i]["go_id"]
                            p_value_str = bp_data[i]["p_value"]
                            score = score_function(distance=distance, p_value_str=p_value_str)
                            if ans_bp_dict.__contains__(go_id):
                                ans_bp_dict[go_id] += score
                            else:
                                ans_bp_dict[go_id] = score
                        file.close()
    tmp = sorted(ans_bp_dict.items(), key = lambda kv:kv[1], reverse=True)
    length = len(tmp)
    ans_bp_list = []
    for i in range(length):
        ans_bp_list.append(tmp[i][0])
    protein = protein_dict["protein"]
    file = open(os.path.join('protein-predict-bp-list-all', protein + '-predict-bp-list-all.txt'), 'w')
    for i in ans_bp_list:
        file.write(i + '\n')
    file.close()
    print(protein + ' finish')

def solve():
    file = open("test_protein_list.txt", "r")
    str_para_list = sys.argv[1:]
    para_list = []
    for str_para in str_para_list:
        para_list.append(int(str_para))
    start_line_id = para_list[0]
    end_line_id = para_list[1]
    cnt = 0
    todo_protein_list = []
    for line in file.readlines():
        cnt += 1
        if cnt < start_line_id:
            continue
        if cnt > end_line_id:
            continue
        protein = line[:-1]
        todo_protein_list.append(protein)
    file.close()

    num = end_line_id - start_line_id + 1
    for i in range(num):

        if not os.path.exists(os.path.join("test-protein-to-vector", todo_protein_list[i] + ".json")):
            print("file", os.path.join("test-protein-to-vector", todo_protein_list[i] + ".json"), "not found")

        file = open(os.path.join("test-protein-to-vector", todo_protein_list[i] + ".json"), "r")
        protein_dict = json.load(file)
        file.close()
        print("calculating line: " + str(start_line_id + i))
        calculate(protein_dict=protein_dict)
    file = open(str(start_line_id) + '-' + str(end_line_id) + '.txt', 'w')
    for x in score_list:
        file.write(x[0] + ' ' + x[1] + '\n')
    file.close()

if __name__ == "__main__":
    solve()