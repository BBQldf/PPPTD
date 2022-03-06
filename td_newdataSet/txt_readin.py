
import os
import numpy as np
from copy import deepcopy


def see_0():
    for i in range(0, 60*24, 15):
        with open("result_final/result_mean_" + str(i) + ".txt") as f:
            for line in f:
                line = line.split(" ")
                if line[3] == "0.0":
                    print(i, line[0])


def maxminnorm(_data):
    _data = np.array(_data)
    maxcols=_data.max(axis=0)
    mincols=_data.min(axis=0)
    data_shape = _data.shape
    data_rows = data_shape[0]
    data_cols = data_shape[1]
    t=np.empty((data_rows,data_cols))
    for i in range(data_cols):
        t[:, i] = (_data[:, i] - mincols[i]) / (maxcols[i] - mincols[i])
    return t

def txt_read(ti):
    path = "./result_final/result_mean_"  # 指定需要读取文件的目录
    print(ti)           # 在这里记录一下时间戳
    data = list()
    count = 0
    with open(path + str(ti*15) + '.txt') as file_obj:      # 读附和要求的文件（4个观测值,50个用户）
        print(path + str(ti*15) + '.txt')
        for line in file_obj:
            line = line.strip('\n')
            line = line.split(' ')
            if line[3] == "0.0":
                continue
            line = list(map(float, line))
            data.append(line[1:])
            count += 1
            if count == 50:
                break
    return list(maxminnorm(data))

# print(txt_read(32))


def Threedimension_Init(m,n,q,x):  #三维数组 M x N x Q 初值是x
    onedimension = []
    twodimension = []
    threedimension = []
    for i in range(m):
        twodimension[:] = []
        for j in range(n):
            onedimension[:] = []
            for k in range(q):
                onedimension.append(x)
            onedimension = deepcopy(onedimension)
            twodimension.append(onedimension)
        twodimension = deepcopy(twodimension)
        threedimension.append(twodimension)
    return threedimension


def Twodimension_Init(m,n,x):  #二维数组 M x N初值是x
    onedimension = []
    twodimension = []
    for i in range(m):
        onedimension[:] = []
        for j in range(n):
            onedimension.append(x)
        onedimension = deepcopy(onedimension)           #解决列表浅复制问题，即高维数组中的每个元素实际上都是同一个低维数组，当有一个低维数组被修改，高维数组中的其他低维数组也跟着被修改了，即“牵一发而动全身”。
        twodimension.append(onedimension)               #deepcopy
        #print(id(twodimension),id(onedimension))
    return twodimension


if __name__ == '__main__':
    for ti in range(80):
        datas = txt_read(ti)
        with open("./result_normalization/result_"+str(ti)+".txt","w+") as f:
            for data in datas:
                value = ', '.join(map(str, data))
                f.write(value+'\n')
