import os
import csv
import json

def solve0():
    file = open(os.path.join('training-ultrapse-file', '2-0.05.txt'), "r")
    training_protein_list = []
    for line in file.readlines():
        list1 = line.split(' ')
        training_protein_list.append(list1[-1][3:])
    file.close()

    file = open("training_protein_list.txt", "w")
    for protein in training_protein_list:
        file.write(protein)
    file.close()

    file = open(os.path.join('test-ultrapse-file', '2-0.05.txt'), "r")
    test_protein_list = []
    for line in file.readlines():
        list1 = line.split(' ')
        test_protein_list.append(list1[-1][3:])
    file.close()

    file = open("test_protein_list.txt", "w")
    for protein in test_protein_list:
        file.write(protein)
    file.close()

ans1 = []
ans2 = []

def solve1():
    global ans1
    file = open("training_protein_list.txt", "r")
    for line in file.readlines():
        protein = line[:-1]
        dict1 = {}
        dict1["protein"] = protein
        dict1["vector_list"] = {}
        ans1.append(dict1)
    file.close()

    file = open("test_protein_list.txt", "r")
    for line in file.readlines():
        protein = line[:-1]
        dict2 = {}
        dict2["protein"] = protein
        dict2["vector_list"] = {}
        ans2.append(dict2)    
    file.close()

def attach_vector_to_protein(training_ultrapse_file_path, test_ultrapse_file_path, para):
    file = open(training_ultrapse_file_path, "r")
    cnt = 0
    for line in file.readlines():
        list1 = line.split(' ')
        vector = []
        for num in list1[:-1]:
            vector.append(float(num))
        ans1[cnt]["vector_list"][para] = vector
        cnt += 1
    file.close()

    file = open(test_ultrapse_file_path, "r")
    cnt = 0
    for line in file.readlines():
        list1 = line.split(' ')
        vector = []
        for num in list1[:-1]:
            vector.append(float(num))
        ans2[cnt]["vector_list"][para] = vector
        cnt += 1
    file.close()

def solve2():
    global ans1, ans2
    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            para_w = para_w_ / 100
            file_name = str(para_l) + '-' + str('%.2f' % para_w) + '.txt'
            print(file_name)
            training_ultrapse_file_path = os.path.join('training-ultrapse-file', file_name)
            test_ultrapse_file_path = os.path.join('test-ultrapse-file', file_name)
            attach_vector_to_protein(training_ultrapse_file_path=training_ultrapse_file_path, test_ultrapse_file_path=test_ultrapse_file_path, para=str(para_l) + '-' + str('%.2f' % para_w))

    # file = open("training-protein-to-vector.json", "w")
    # json.dump(ans1, file)
    # file.close()
    for protein_dict in ans1:
        file = open(os.path.join("training-protein-to-vector", protein_dict["protein"] + ".json"), "w")
        json.dump(protein_dict, file)
        file.close()
    # file = open("test-protein-to-vector.json", "w")
    # json.dump(ans2, file)
    # file.close()
    for protein_dict in ans2:
        file = open(os.path.join("test-protein-to-vector", protein_dict["protein"] + ".json"), "w")
        json.dump(protein_dict, file)
        file.close()

if __name__ == "__main__":
    solve0()
    solve1()
    solve2()
