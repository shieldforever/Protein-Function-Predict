import os
import csv
import json
import math
import sys

test_protein_to_vector_list = []
front_num = 0

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
    

def test(protein, ans_list, go):
    file = open("real-protein-go-ranklist.json", "r")
    real_protein_go_ranklist_dict = json.load(file)
    file.close()
    if not real_protein_go_ranklist_dict.__contains__(protein):
        print('---------', protein, go, "real protein list not found!")
        return
    real_protein_go_ranklist = real_protein_go_ranklist_dict[protein]
    real_list = real_protein_go_ranklist[go]
    real_length = len(real_list)
    in_cnt = 0

    for i in range(real_length):
        if real_list[i] in ans_list:
            in_cnt += 1
    global score_list
    if real_length == 0:
        print('---------', protein, go, "accuracy: ", "no real go terms")
        score_list.append([protein, "no real go terms"])
    else:
        accuracy = float(float(in_cnt) / real_length)
        print('---------', protein, go, "accuracy: ", "%.6f%%" % (accuracy * 100.0))
        score_list.append([protein, "%.6f%%" % (accuracy * 100.0)])
    
def solve():
    file = open("test_protein_list.txt", "r")
    str_para_list = sys.argv[1:]
    para_list = []
    for str_para in str_para_list:
        para_list.append(int(str_para))
    start_line_id = para_list[0]
    end_line_id = para_list[1]
    length = para_list[2]
    global front_num
    cnt = 0
    front_num = 10
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
        # print("calculating " + todo_protein_list[i])
        print(start_line_id + i)
        file = open(os.path.join('protein-predict-cc-list-all', todo_protein_list[i] + '-predict-cc-list-all.txt'), 'r')
        all_ans_list = []
        for line in file.readlines():
            all_ans_list.append(line[:-1])
        ans_list = all_ans_list[:length]
        test(protein=todo_protein_list[i], ans_list=ans_list, go='real_cc_go_list')
    
    file = open('cc-' + str(start_line_id) + '-' + str(end_line_id) + '-' + str(length) + '.txt', 'w')
    for x in score_list:
        file.write(x[0] + ' ' + x[1] + '\n')
    file.close()

if __name__ == "__main__":
    solve()