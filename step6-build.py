import os
import csv
import json

def calculate_center_vector(file_path, gene_to_vector_filepath, go_p_file_path, cluster_name, target_file_path):
    file = open(file_path, 'r')
    gene_list = []
    for line in file.readlines():
        gene = line[:-1]
        gene_list.append(gene)
    file.close()

    gene_to_vector_dict = {}
    file= open(gene_to_vector_filepath, "r")
    for line in file.readlines():
        list1 = line.split(' ')
        vector = []
        for num in list1[:-1]:
            vector.append(float(num))
        gene = list1[-1][3:-1]
        gene_to_vector_dict[gene] = vector    
    file.close()

    vector_list = []
    for gene in gene_list:
        vector = gene_to_vector_dict[gene]
        vector_list.append(vector)
    
    dimension = len(vector_list[0])
    center_vector = [0] * dimension
    for vector in vector_list:
        for i in range(dimension):
            center_vector[i] += vector[i]
    vector_num = len(vector_list)
    for i in range(dimension):
        center_vector[i] /= vector_num
    
    dict1 = {}
    dict1['cluster_name'] = cluster_name
    dict1['vector'] = center_vector
    dict1['data'] = []

    file = open(go_p_file_path, "r")
    reader = csv.reader(file)
    result = list(reader)
    for i in range(1, len(result)):
        list1 = result[i]
        go_id = list1[0]
        p_value = list1[4]
        dict2 = {}
        dict2['go_id'] = go_id
        dict2['p_value'] = p_value
        dict1['data'].append(dict2)
    file.close()

    file = open(target_file_path, "w")
    json.dump(dict1, file)
    file.close()


if __name__ == "__main__":
    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            para_w = para_w_ / 100
            for para_k in range(10, 45, 5):
                for num_of_neighbor in range(150, 160, 10):
                    file_folder_name = str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor)
                    print("reading:", file_folder_name)
                    file_folder_path = os.path.join('spectral-cluster-file', file_folder_name)
                    for i in range(0, para_k):

                        file_path = os.path.join(file_folder_path, str(i) + '.txt')

                        cc_go_p_file_path = os.path.join('cc-go-p-result', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor), str(i) + '.csv')
                        bp_go_p_file_path = os.path.join('bp-go-p-result', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor), str(i) + '.csv')
                        mf_go_p_file_path = os.path.join('mf-go-p-result', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor), str(i) + '.csv')

                        gene_to_vector_filepath = os.path.join('training-ultrapse-file', str(para_l) + '-' + str('%.2f' % para_w) + '.txt')

                        cc_target_file_path = os.path.join('cc-data', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor) + '-' + str(i) + '.json')
                        bp_target_file_path = os.path.join('bp-data', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor) + '-' + str(i) + '.json')
                        mf_target_file_path = os.path.join('mf-data', str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor) + '-' + str(i) + '.json')

                        calculate_center_vector(file_path=file_path, gene_to_vector_filepath=gene_to_vector_filepath, go_p_file_path=cc_go_p_file_path, cluster_name=file_folder_name+'-'+str(i), target_file_path=cc_target_file_path)
                        calculate_center_vector(file_path=file_path, gene_to_vector_filepath=gene_to_vector_filepath, go_p_file_path=bp_go_p_file_path, cluster_name=file_folder_name+'-'+str(i), target_file_path=bp_target_file_path)
                        calculate_center_vector(file_path=file_path, gene_to_vector_filepath=gene_to_vector_filepath, go_p_file_path=mf_go_p_file_path, cluster_name=file_folder_name+'-'+str(i), target_file_path=mf_target_file_path)
