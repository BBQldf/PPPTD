import sympy
import random
import time

from copy import deepcopy

from users import perturbation
#from server import Weight_Computation,adaptive_sample,Weight_Computation1
from server import adaptive_sample,Weight_Computation1,Weight_Computation
from estimation import MAE,MAPE,MAE2,MAPE2
from txt_readin import txt_read,Twodimension_Init,Threedimension_Init
import numpy as np
#from server_test import Weight_Computation,Weight_Computation_WE




alpha=0.54
beta = 0.37             #关于隐私分配的用户调查模型

#maxepsiono = 0.03    #这个值还不确定，先赋值一个
maxepsiono = 0.03
w=[]            #表示时间戳中，所有用户对应的weight，是一个二维数组
wwe = []
scale=[]               #epsiono是用户端传上来的，也需要维护一个表吧？每一个用户对应着一个epsiono，同时也有时间标签，
                        #同时对于每一个用户的不同任务也不一样， 所以是一个三维数组
scalewe=[]
epsionoall = []  # 一维数组，记录每一个用户对应的epsiono

lamuda =0.6        #预定义的lamuda值，决定最开始的隐私分配


# def timeDistribute():                   #将得到的数据集按时间戳进行分配
#     with open(file_path) as file_object:


def TimeAllocate():
                #对每个时间戳进行调度运行，server端运行动态budget调整，和权值估计，以及真值发现；user端进行加噪
    global alpha, beta, w,scale,lamuda,scalewe,wwe,epsionoall

    #先进行初始化操作——epsiono和weight

    A = PrivacyLevelConfirmation(lamuda, rate=1 - alpha)
    B = PrivacyLevelConfirmation(lamuda, rate=1 - alpha - beta)  # k值越大，A/B的值越小，最小为0.5；
    epsionoall ,epsionolist=initial(maxepsiono, A, B)           #这里不需要返回值，epsiono和weight都是全局变量


    #从第一个时间戳开始，先对用户加噪
    xi=[]           #记录加噪后的数据，是一个二维数组
    xiwe = []  # 记录加噪后的数据，是一个二维数组
    tilast = 0      #记第一个更新点为tilast
    tilastwe = 0  # 记第一个更新点为tilast
    Mae =[]         #用一个以为数组记录20个时间点内，所有的mae值，然后求平均
    Maewe = []  # 用一个以为数组记录20个时间点内，所有的mae值，然后求平均
    Mape = []  # 用一个以为数组记录20个时间点内，所有的mape值，然后求平均
    Mapewe = []  # 用一个以为数组记录20个时间点内，所有的mape值，然后求平均
    Zall = []  # 所有时间戳的，所有objects的真值
    Zallwe = []
    adaptive_user = 0
    for ti in range(79):        #先考虑有20个时间戳
        originals = []      #原始数据，二维数组，user_obj

        originals = txt_read(ti)

        xi=perturbation(scale,originals,ti)
        scale,tilast,objectaita,adaptive_user=adaptive_sample(tilast,ti,scale,w,epsionolist,adaptive_user)
        #Zall,sumepsiono1 = Weight_Computation(xi, ti, scale, w, Zall)  # w考虑返回
        Zall, sumepsiono1 = Weight_Computation1(xi, ti, scale, w, Zall)

        # first = MAE2(Zall, originals, ti)            #求这个时间戳下的mae
        # Mae.append(first)
        # second = MAPE2(Zall, originals, ti)          #求这个时间戳下的mape
        # Mape.append(second)

        #xiwe = perturbation(scalewe, originals, ti)
        # Zallwe,sumepsiono2 = Weight_Computation1(xi, ti, scalewe, wwe, Zallwe)      #这里scale不参与计算，只是用来算sumepsiono
        #Zallwe = Weight_Computation1(xiwe, ti, scalewe, wwe, Zallwe)
        #Zallwe = Weight_Computation1(xi, ti, scalewe, wwe,Zallwe)  # w考虑返回

        #epsionowe, tilastwe = adaptive_sample(tilastwe, ti, epsionowe, wwe)

        # firstwe = MAE2(Zallwe, originals, ti)  # 求这个时间戳下的mae
        # Maewe.append(firstwe)
        # secondwe = MAPE2(Zallwe, originals, ti)  # 求这个时间戳下的mape
        # Mapewe.append(secondwe)
        #
        # # print("second:", second)
        # print("secondwe:", secondwe)
        #供调试用
    #    print("对应的用户权重为：",w[ti])
        print("******************************\n")


    # np.savetxt(".//data//Mae.txt", Mae)
    # np.savetxt(".//data//Maewe.txt", Maewe)
    # np.savetxt(".//data//Mape.txt", Mape)
    # np.savetxt(".//data//Mapewe.txt", Mapewe)

    # first1=sumW(Mae)            #求整个时间段内，总的mae值
    # first1 = first1/len(Mae)    #求每个时间段的平均误差
    # print(first1)
    # second1=sumW(Mape)
    # second1 = second1/len(Mape)       #求平均，用于作图
    # print(second1)
    # with open('.//data//first1.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(first1)+'\n'+str(second1))

    # first1we=sumW(Maewe)            #求整个时间段内，总的mae值
    # first1we = first1we/len(Maewe)    #求每个时间段的平均误差
    # print(first1we)
    # second1we=sumW(Mapewe)
    # second1we = second1we/len(Mapewe)       #求平均，用于作图
    # print(second1we)
    # with open('.//data//first1we.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(first1we)+'\n'+str(second1we))

    # with open('.//data//result.txt', 'a+', encoding='utf-8') as f:
    #     f.write(str(sumepsiono2) + '\n' + str(sumepsiono1) + '\n' + str(first1) + '\n' + str(first1we)+ '\n' + str(second1)+ '\n' + str(second1we)+ '\n'+ '\n')

    # with open('.//data//adaptive_user.txt', 'a', encoding='utf-8') as f:
    #     f.write(str(adaptive_user)+'\n')

def initial(maxepsiono,A,B):
    #对epsiono需要全部赋值；第一次的weight值也是在这里赋值
    global alpha,beta,w,wwe,scale,scalewe
    sensitivity = 0.01        #预定义的任务敏感度，所有数据都是天气温度，敏感度一致，设为5
    timestamps = 80    #预定义的时间戳范围
    users = 100     #预定义的用户数
    objects = 50     #预定义的任务数量
    epsiono1 = random.uniform(0.002,0.0025)                    #高隐私级别
    epsiono2 = random.uniform((A/B)*maxepsiono-0.003,(A/B)*maxepsiono-0.0015)     #这里的范围也需要进一步确定
    epsiono3 = maxepsiono                                            #最大的epsiono值

    epsionolist =[epsiono1,epsiono2,epsiono3]

    #pivot = beta/(alpha+beta)
    timestamp =0            #初始化的时候先只对ti=0时刻进行初始化，epsiono后面的时候均复制
    for user in range(users):             #这是随机选择用户隐私需求，但是对用户较少的情况下，有点不那么随机；先放在这里，留作备用
        ratio = random.random()
        if ratio < alpha :                     #高隐私需求
            for object in range(objects):
                scale[timestamp][user][object] =  sensitivity/epsiono1
            epsionoall.append(epsiono1)
        elif ratio < beta+alpha :                         #中隐私需求
            for object in range(objects):
                scale[timestamp][user][object] = sensitivity/ epsiono2
            epsionoall.append(epsiono2)
        else:                                               #低隐私需求
            for object in range(objects):
                scale[timestamp][user][object] = sensitivity/ epsiono3
            epsionoall.append(epsiono3)             #保存每一用户对应的epsiono的值

    # for user in range(users):             #这是随机选择用户隐私需求，但是对用户较少的情况下，有点不那么随机.设定前3个高隐私，第4个中隐私，第5个低隐私
    #     if user < 3:                     #高隐私需求
    #         for object in range(objects):
    #             scale[timestamp][user][object] =  sensitivity[object]/epsiono1
    #     elif user < 4:                         #中隐私需求
    #         for object in range(objects):
    #             scale[timestamp][user][object] = sensitivity[object] / epsiono2
    #     else:                                               #低隐私需求
    #         for object in range(objects):
    #             scale[timestamp][user][object] = sensitivity[object] / epsiono3
    #
    # for user in range(users):  # 这是随机选择用户隐私需求，但是对用户较少的情况下，有点不那么随机.设定前3个高隐私，第4个中隐私，第5个低隐私
    #     if user < 3:  # 高隐私需求
    #         for object in range(objects):
    #             scalewe[timestamp][user][object] = sensitivity[object] / epsiono1
    #     elif user < 4:  # 中隐私需求
    #         for object in range(objects):
    #             scalewe[timestamp][user][object] = sensitivity[object] / epsiono2
    #     else:  # 低隐私需求
    #         for object in range(objects):
    #             scalewe[timestamp][user][object] = sensitivity[object] / epsiono3
    for user in range(users):
        # if random.random() < alpha:  # 高隐私需求
        #     for object in range(objects):
        #         scalewe[timestamp][user][object] = sensitivity / epsiono1
        # elif random.random() < beta:  # 中隐私需求
        #     for object in range(objects):
        #         scalewe[timestamp][user][object] = sensitivity / epsiono2
        # else:  # 低隐私需求
        #     for object in range(objects):
        #         scalewe[timestamp][user][object] = sensitivity / epsiono3
        w[0][user] = 1/users            #第一次都是均分的weight
        wwe[0][user] = 1 / users  # 第一次都是均分的weight

        for timestamp in range(1,timestamps):    #初始化的时候epsiono在每个时间戳下，对于同一用户的隐私预算应该是一样的
            scale[timestamp]=scale[0]                           #这里没有用deepcopy是正确的，这样可以让所有的时间戳同时全部更新
            scalewe[timestamp] = scalewe[0]

    scalewe = deepcopy(scale)                               #这里保证了scalewe的更新不和scale同步，即以后只是scale在更新，而scalewe保持在初始化的状态

    return epsionoall,epsionolist



def PrivacyLevelConfirmation(k, rate):            #最开始的根据用户隐私级别的budget分割
    x1 = 0
    x2 = 1
    x = sympy.Symbol('x')
    t = sympy.Symbol('t')
    f = k*sympy.E**(-k*x)
    f1 = sympy.integrate(f, (x, x1, t))/sympy.integrate(f, (x, x1, x2))-(1-rate)
    return sympy.solve(f1)[0]

# A=PrivacyLevelConfirmation(0.1, rate=1-alpha)
# B=PrivacyLevelConfirmation(0.1, rate=1-alpha-beta)       # k值越大，A/B的值越小，最小为0.5；
#print(A,B,A/B)

def sumW(w):            #求某一时间t所有用户的权值总和，传入的是w[ti]，一维数组
    usersweight=0
    for weight in range(len(w)):
        usersweight = usersweight + w[weight]
    return usersweight                      #返回总的权值之和


if __name__ == '__main__':
    t = 100
    singleT = []
    times_start = time.time()
    while t>0:
        w = Twodimension_Init(80,100,0.0625)   #20个时间戳5个users，初值为0.01
        wwe = Twodimension_Init(80, 100, 0.0625)  # 20个时间戳5个users，初值为0.01
        scale = Threedimension_Init(80,100,50,0.0001)        #20个时间戳5个user6个objects，初值为0.0001
        scalewe = Threedimension_Init(80, 100, 50, 0.0001)  # 20个时间戳5个user6个objects，初值为0.0001
        single_timestrat = time.time()
        TimeAllocate()
        single_timeend = time.time()
        t = t -1
        singleT.append(single_timeend-single_timestrat)

    times_end = time.time()
    print('totally cost',times_end-times_start)
    print("单轮：",singleT)
    # w = Twodimension_Init(80,100,0.0625)   #20个时间戳5个users，初值为0.01
    # wwe = Twodimension_Init(80, 100, 0.0625)  # 20个时间戳5个users，初值为0.01
    # scale = Threedimension_Init(80,100,50,0.0001)        #20个时间戳5个user6个objects，初值为0.0001
    # scalewe = Threedimension_Init(80, 100, 50, 0.0001)  # 20个时间戳5个user6个objects，初值为0.0001
    # TimeAllocate()