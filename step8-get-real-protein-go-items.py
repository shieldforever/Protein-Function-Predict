import os
import json
import csv

# real-protein-go-ranklist
model_go_dict = {}

def getinfo(s):
    ans_list = []
    go_s_list = s.split(';')
    for go_s in go_s_list:
        l = go_s.find('[')
        r = go_s.find(']')
        if l == -1 or r == -1:
            pass
        else:
            go_id = go_s[l+1:r]
            if model_go_dict.get(go_id) == None:
                pass
            else:
                ans_list.append(go_id)
    return ans_list



def solve():
    file = open("GO-BP-CC-MF.csv", "r")
    reader = csv.reader(file)
    result = list(reader)
    real_protein_go_ranklist = {}
    for protein_info in result[1:]:
        protein = protein_info[0]
        real_protein_go_ranklist[protein] = {}
        real_protein_go_ranklist[protein]["real_mf_go_list"] = getinfo(protein_info[2])
        real_protein_go_ranklist[protein]["real_cc_go_list"] = getinfo(protein_info[3])
        real_protein_go_ranklist[protein]["real_bp_go_list"] = getinfo(protein_info[4])

    file.close()
    file = open("real-protein-go-ranklist.json", "w")
    json.dump(real_protein_go_ranklist, file)
    file.close()

if __name__ == "__main__":
    file = open('model-cc-go.txt', 'r')
    for line in file.readlines():
        model_go_dict[line[:-1]] = 1
    file.close()
    file = open('model-bp-go.txt', 'r')
    for line in file.readlines():
        model_go_dict[line[:-1]] = 1
    file.close()
    file = open('model-mf-go.txt', 'r')
    for line in file.readlines():
        model_go_dict[line[:-1]] = 1
    file.close()
    print(model_go_dict.__sizeof__())
    solve()