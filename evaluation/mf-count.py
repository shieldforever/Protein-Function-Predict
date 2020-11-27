import os

for i in range(10, 20, 10):
    no_num = 0
    cnt = 0
    v = float(i)
    file = open('mf-1-2034-100.txt', 'r')
    for line in file.readlines():
        x = line.split(' ')
        if x[1] == 'no':
            no_num += 1
        else:
            xx = eval(x[1][:-2])
            if xx >= v:
                cnt += 1
    file.close()
    print("no real mf go items: " + str(no_num))


# v = float(input("input the min accuracy: "))
for i in range(10, 110, 10):
    no_num = 0
    cnt = 0
    v = float(i)
    file = open('mf-1-2034-100.txt', 'r')
    for line in file.readlines():
        x = line.split(' ')
        if x[1] == 'no':
            no_num += 1
        else:
            xx = eval(x[1][:-2])
            if xx >= v:
                cnt += 1
    file.close()
    # print("no real mf go items: " + str(no_num))
    print('number of protein prediction accuracy greater than ' + str(v) + ': ' + str(cnt))