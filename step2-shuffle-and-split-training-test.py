import os
import random
import numpy as np

dict = {}
total_num = 0
gene_num = 0

def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        os.remove(file_path)

def write_vec_into_file(vec, new_file):
    is_head = True
    s = ''
    for word in vec:
        if is_head:
            s = s + str(word)
        else:
            s = s + ' ' + str(word)
        is_head = False
    new_file.write(s)

def push_dict(key):
    if key in dict.keys():
        value = dict.get(key)
        dict[key] = value + 1
    else:
        dict[key] = 1

def create_dict_for_one_file(origin_ultrapse_file_path):
    file = open(origin_ultrapse_file_path, 'r')
    for l in file.readlines():
        ll = "".join(l)
        line = ll.split(' ')
        vec = []
        nan_flag = True
        for word in line:
            i = 0
            while i < len(word) and word[i] != ':':
                i = i + 1
            if i == len(word):
                continue
            num = float(word[i + 1 : ])
            if np.isnan(num):
                nan_flag = False
                break
            vec.append(num)
        if nan_flag == False:
            continue
        push_dict(key=line[-1])
    file.close()

def write_work(origin_ultrapse_file_path, training_ultrapse_file_path, test_ultrapse_file_path, gene_list):
    file = open(origin_ultrapse_file_path, 'r')
    gene_info_dict = {}
    for l in file.readlines():
        ll = "".join(l)
        line = ll.split(' ')
        vec = []
        nan_flag = True
        for word in line:
            i = 0
            while i < len(word) and word[i] != ':':
                i = i + 1
            if i == len(word):
                continue
            num = float(word[i + 1 : ])
            if np.isnan(num):
                nan_flag = False
                break
            vec.append(num)
        if nan_flag == False:
            continue
        vec.append(line[-1])
        if dict.get(line[-1]) == total_num:
            gene_info_dict[line[-1]] = vec
    file.close()
    print(len(gene_list))

    new_training_file = open(training_ultrapse_file_path, 'w')

    training_num = int(len(gene_list) * 0.9)
    for i in range(0, training_num):
        gene_name = gene_list[i]
        vec = gene_info_dict.get(gene_name)
        write_vec_into_file(vec, new_training_file)
    print(training_ultrapse_file_path + ' finished')
    new_training_file.close()

    new_test_file = open(test_ultrapse_file_path, 'w')
    test_num = len(gene_list) - training_num
    for i in range(training_num, training_num + test_num):
        gene_name = gene_list[i]
        vec = gene_info_dict.get(gene_name)
        write_vec_into_file(vec, new_test_file)
    print(test_ultrapse_file_path + ' finished')
    new_test_file.close()

def create_dict():
    # 统计不同参数下，每个基因出现的次数
    global total_num
    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            total_num = total_num + 1
            para_w = para_w_ / 100
            ultrapse_file_name = str(para_l) + '-' + str('%.2f' % para_w) + '.txt'
            origin_ultrapse_file_path = os.path.join('ultrapse-file-origin', ultrapse_file_name)
            create_dict_for_one_file(origin_ultrapse_file_path=origin_ultrapse_file_path)

def gene_shuffle_and_data_separate_and_write():
    global gene_num
    gene_list = []
    for key in dict.keys():
        value = dict.get(key)
        if value == total_num:
            gene_num = gene_num + 1
            gene_list.append(key)
    for i in range(gene_num - 1, 0, -1):
        x = random.randint(0, i)
        # swap
        tmp = gene_list[i]
        gene_list[i] = gene_list[x]
        gene_list[x] = tmp
    
    if not os.path.exists("training-ultrapse-file"):
        os.system("mkdir training-ultrapse-file")
    del_file("training-ultrapse-file")
    if not os.path.exists("test-ultrapse-file"):
        os.system("mkdir test-ultrapse-file")
    del_file("test-ultrapse-file")

    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            para_w = para_w_ / 100
            ultrapse_file_name = str(para_l) + '-' + str('%.2f' % para_w) + '.txt'
            origin_ultrapse_file_path = os.path.join('ultrapse-file-origin', ultrapse_file_name)
            training_ultrapse_file_path = os.path.join('training-ultrapse-file', ultrapse_file_name)
            test_ultrapse_file_path = os.path.join('test-ultrapse-file', ultrapse_file_name)

            write_work(origin_ultrapse_file_path=origin_ultrapse_file_path, training_ultrapse_file_path=training_ultrapse_file_path, test_ultrapse_file_path=test_ultrapse_file_path, gene_list=gene_list)

if __name__ == "__main__":
    create_dict()
    gene_shuffle_and_data_separate_and_write()