import numpy as np
import os
import time
from sklearn import datasets
from sklearn.cluster import SpectralClustering
from sklearn import metrics
import sys

def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        os.remove(file_path)

def get_data(ultrapse_file_path):
    file = open(ultrapse_file_path, 'r')
    data = []
    pr = []
    for l in file.readlines():
        ll = "".join(l)
        line = ll.split(' ')
        pr.append(line[-1])
        vec = []
        length = len(line)
        for i in range(0, length - 1):
            vec.append(float(line[i]))
        data.append(vec)
    return (data, pr)

def Calc_Spectral_Clustering(data, pr, para_l, para_w, para_k, num_of_neighbor):
    print("Is calculating... num_of_neighbor=", num_of_neighbor, "n_cluster=", para_k)
    print('begin time: ' + time.strftime('%Y-%m-%d %H:%M:%S'))
    nd_data = np.array(data)
    pred_y = SpectralClustering(n_clusters=para_k, affinity='nearest_neighbors', n_neighbors=num_of_neighbor, assign_labels='discretize').fit_predict(nd_data)
    score = metrics.calinski_harabasz_score(nd_data, pred_y)
    print("Calinski-Harabasz Score with num_of_neighbor=", num_of_neighbor, "n_cluster=", para_k, "score=", score)
    print('end time: ' + time.strftime('%Y-%m-%d %H:%M:%S'))

    data = nd_data.tolist()
    y_label = pred_y.tolist()
    results = []
    i = 0
    for line in data:
        row = []
        row.append(y_label[i])
        row.append(line)
        row.append(pr[i])
        results.append(row)
        i += 1
    results = sorted(results, key = (lambda x:x[0]))
    
    file_folder_name = str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor)
    file_folder = os.path.join("spectral-cluster-file", file_folder_name)
    if not os.path.exists(file_folder):
        os.system('mkdir ' + file_folder)
    del_file(file_folder)
    print('writing into spectral-cluster-file')

    f = open(os.path.join(file_folder, 'score.txt'), 'w')
    f.write(str(score) + '\n')
    f.close()

    f = open(os.path.join(file_folder, '0.txt'), 'w')
    num = 0
    p = 0
    for result in results:
        p += 1
        if num != result[0]:
            f.close()
            num = result[0]
            f=open(os.path.join(file_folder, str(num) + '.txt'), 'w')
        f.write(result[2][3:])
        f.flush()
    f.close()

def make_parameter():
    f = open('parameter.txt', 'w')
    # str_para_list = sys.argv[1:]
    # para_list = []
    # for str_para in str_para_list:
    #     para_list.append(int(str_para))

    # if not os.path.exists("spectral-cluster-file"):
    #     os.system("mkdir spectral-cluster-file")
    # del_file("spectral-cluster-file")

    # for para_l in range(para_list[0], para_list[1], 1):
    #     for para_w_ in range(para_list[2], para_list[3], 5):
    #         para_w = para_w_ / 100
    #         ultrapse_file_name = str(para_l) + '-' + str('%.2f' % para_w) + '.txt'
    #         ultrapse_file_path = os.path.join('training-ultrapse-file', ultrapse_file_name)
    #         data, pr = get_data(ultrapse_file_path=ultrapse_file_path)
    #         print(ultrapse_file_name + ' finished')
    #         for para_k in range(para_list[4], para_list[5], 10):
    #             for num_of_neighbor in range(para_list[6], para_list[7], 10):
    #                 print(str(para_l) + '-' + str('%.2f' % para_w) + '-' + str(para_k) + '-' + str(num_of_neighbor))
    #                 Calc_Spectral_Clustering(data=data, pr=pr, para_l=para_l, para_w=para_w, para_k=para_k, num_of_neighbor=num_of_neighbor)
    for para_l in range(2, 16, 1):
        for para_w in range(5, 85, 5):
            # para_w = para_w_ / 100
            # ultrapse_file_name = str(para_l) + '-' + str('%.2f' % para_w) + '.txt'
            # ultrapse_file_path = os.path.join('ultrapse-file', ultrapse_file_name)
            # data, pr = get_data(ultrapse_file_path=ultrapse_file_path)
            # print(ultrapse_file_name + ' finished')
            for para_k in range(10, 45, 5):
                # for num_of_neighbor in range(30, 160, 10):
                f.write(str(para_l) + ' ' + str(para_w) + ' ' + str(para_k) + ' ' + str(150) + '\n')
                # Calc_Spectral_Clustering(data=data, pr=pr, para_l=para_l, para_w=para_w, para_k=para_k, num_of_neighbor=num_of_neighbor)
    f.close()
if __name__ == "__main__":
    make_parameter()