import os
import csv

DATA_PATH = "./case3"
file_a = DATA_PATH + "pressure-outlet2.dpm"

a_list = []
result = []
exit_sum = 0
raw_num = 0

with open(file_a) as f:
    while True:
        tmp = f.readline()
        if not tmp:
            break

        line = tmp[170:-2]
        raw_num += 1
        if raw_num > 2:
            if a_list.count(line) != 1:
                a_list.append(line)

for num in range(2,10):
    file_b = DATA_PATH + "ryouiki{}.dpm".format(num)
    exit_count = 0
    old_temp = ""
    list_num = ["領域{}".format(num)]
    with open(file_b) as h:
        while True:
            judg = 0
            tmp = h.readline()
            if not tmp:
                result.append(exit_count)
                break
            line = tmp[170:-2]
            judg = a_list.count(line)
            if judg == 1:
                exit_count += 1
                exit_sum += 1
                a_list.remove(line)
                list_num.append(tmp[146:156])

    print("領域 {}から"。format(num) + str(result[num -2]))

    with open("流出時間.csv" , "a") as z:
        writer = csv.writer(z , lineterminator = "\n")
        writer.writerow(list_num)

print("流出粒子の合計は：" , exit_sum)
print(result)