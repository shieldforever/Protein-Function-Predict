import time
import os

def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        os.remove(file_path)

def part1():
    origin_file_name = input("Please input the name of the input file(If you do not put the input file in the 'origin-data' folder, you should input the path of the input file): ")
    para_t = 2
    # para_l 2-15      14
    # para_w 0.05-0.8  16
    if not os.path.exists("ultrapse-file-origin"):
        os.system("mkdir ultrapse-file-origin")
    del_file("ultrapse-file-origin")
    for para_l in range(2, 16, 1):
        for para_w_ in range(5, 85, 5):
            para_w = para_w_ / 100
            target_ultrapse_file_name = str(para_l) + '-' + str('%.2f' % para_w) + '.txt'
            print(str(para_l) + '-' + str('%.2f' % para_w))
            os.system('Windows\\upse -i origin-data\\' + origin_file_name + ' -u Windows\\tdfs\\classic-pseaac.lua ' + '-t ' + str(para_t) + ' -l ' + str(para_l) + ' -w ' + str('%.2f' % para_w) + ' -f svm -v>>' + 'ultrapse-file-origin\\' + target_ultrapse_file_name)

if __name__ == "__main__":
    part1()


