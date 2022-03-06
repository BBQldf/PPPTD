
import os


# 读取


def myRead():

    for (root, dirs, files) in os.walk("D:/test"):
        #print(root,dirs,files)
        for filename in files  :  # 遍历该文件夹下的每个文件
            filePath =os.path.join(root, filename  )  # 完整的路径
            r = open(filePath)
            #last=""
            # 一行行读 去掉换行符号
            # for temp in r.readlines():
            #     temp=temp.strip( ' \n')
            #     last+=temp
            #
            #
            # arr=last.split('   ')  # 保存到数组里面
            # print(filename,"内容为:")
            # print(arr)
            # print(arr[1])
            for line in r.readlines():
                linestr = line.strip()
                print(linestr)
                linestrlist = linestr.split("\t")
                print(linestrlist)
                linelist = map(int, linestrlist)  # 方法一
                print(linelist)
            r.close()
sum= 0


def myWrite(arr):
    global sum
    filePath = "D:/test" + "/" + str(sum) + ".txt"
    sum = sum +1
    with open(filePath, 'w') as f:
        flag = False
        for temp in arr:
            if flag == True:
                f.write(" " + str(temp))
            else:
                flag = True
                f.write(str(temp))

    print("写入完成")
    f.close()


arr = [1, 2, 3, 2, 1]
arr1 = [23.4444, 54]
# myWrite(arr)
# myWrite(arr1)
# myRead()


#python按顺序读取目录下的所有文件
import os

from copy import deepcopy


def txt_read(ti):
    #f = open("./test_name.txt", 'w')  # 先创建一个空的文本
    path = "./result50/"  # 指定需要读取文件的目录
    files = os.listdir(path)  # 采用listdir来读取所有文件
    files.sort()  # 排序
    s = []  # 创建一个空列表,用于承接一个用户的原始数据
    ss = []   #二维列表,表示一个时间戳下，所有用户的所有观测值数据
    print(ti)           #在这里记录一下时间戳
    flag = 0
    cnt = 0         #防止取到重复文件的计数
    while flag == 0:
        for file_ in files[0:100]:  # 循环读取每个文件名        从ti开始(ti+2,是因为前面两个文件不是我们的数据集
            #print(path +file_)

            count = len(open(path +file_, 'rb').readlines())
            #print(count)
            if count == 17:
                cnt += 1
                if cnt <= ti:
                    continue
                else:
                    with open(path + file_,'r') as file_obj:            #读附和要求的文件（16个观测值）
                        next(file_obj)                          #跳过第一行
                        lines = file_obj.readlines()
                        print(path+file_)
                        for line in lines:
                            #print(line)
                            line = line.strip('\n')
                            line =line.split(',')
                            s = deepcopy(s)
                            s[:]=[]         #清理上一用户数据
                            for i in range(1,27):
                                #print(line)
                                #print(line[i])
                                s.append(float(line[i]))        #记录单个用户的观测值

                            ss.append(s)
                        #print(ss)
                break
        break
    return ss

#print(s)  # 看一下列表里的内容

#ss=txt_read(80)
#print(ss)

from copy import deepcopy


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


