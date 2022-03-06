
import os
from copy import deepcopy


def txt_read(ti):
    #f = open("./test_name.txt", 'w')  # 先创建一个空的文本
    path = "./result_final/result_"  # 指定需要读取文件的目录
    s = []  # 创建一个空列表,用于承接一个用户的原始数据
    ss = []   #二维列表,表示一个时间戳下，所有用户的所有观测值数据
    print(ti)           #在这里记录一下时间戳
    with open(path + str(ti) + '.txt','r', encoding='utf-8') as file_obj:            #读附和要求的文件（4个观测值,100个用户）
        lines = file_obj.readlines()
        print(path + str(ti) + '.txt')
        for line in lines[0:100]:
            #print(line)
            line = line.strip('\n')
            line =line.split(' ')
            s = deepcopy(s)
            s[:]=[]         #清理上一用户数据
            for i in range(0,50):
                #print(line)
                #print(line[i])
                #print(i)
                s.append(float(line[i]))        #记录单个用户的观测值
            ss.append(s)
    return ss

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

# result = Threedimension_Init(4,3,3,1.2)
# newres = result[0][0][2]
# newres = 3
# result[1][0][2] = newres
# print(type(result[1][0][2]))

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

