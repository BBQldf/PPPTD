rho = 0.6
PI = 0.02
directory = './/data//lamuda' + str(0.6) + '_adaptive_user//' + str(1) + '_' + str(PI) + '_' + str(
    rho) + '//'

timestamp_data = [] #承接每个时间戳平均更新用户
for ti in range(79):
    with open(directory + str(ti) + '.txt', 'r') as f:
        data = f.readlines()  # txt中所有字符串读入data
    count = 0.0
    for line in data:
        #odom = line.split()  # 将单个数据分隔开存好
        numbers_float = float(line)  # 转化为浮点数
        count  += numbers_float
    average = count/100
    timestamp_data.append(average)
with open(directory + str('timestamps') + '.txt', 'w') as f:
    for time in timestamp_data:
        f.write(str(time)+'\n')

print(timestamp_data)









