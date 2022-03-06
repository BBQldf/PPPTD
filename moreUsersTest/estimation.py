#server需要传入TD之后的用户数据
#同时需要获得原始数据，来求MAE和MRE


def MAE(Zall,originals,ti):         #传入的是这个时间戳的真值(一维列表）和原始值（二维列表，包含用户数和观测数），还有时间戳
    objects=len(Zall[ti])      #计算被观测点的数量
    sum1=[]                 #是一个一维数组
    mae= 0                  #初值为0
    Zti = Zall[ti]         #Zti表示t=i时间戳上，所有objects的真值

    #下面对originals进行真值发现


    # 对每个用户的观测的单个值进行计算，然后需要计算每个用户在每个观测点的误差范围
    for num in range(len(originals)):               #求出用户个数
        user_devite = 0  # 初始的对于单个user，所有的object的误差和
        for obj in range(objects):                         #观测值数目
            user_devite=abs(originals[num][obj]-Zti[obj]) + user_devite      #把每一个object对应的误差值放到sum1中
        #user_devite = user_devite/objects          #先注释掉，因为目前这个单个用户误差并不太大          #除以objects的数目，指对于单个用户而言，它的误差是多少
        sum1.append(user_devite)
    for sumall in sum1:
        mae = sumall + mae
    mae = mae/len(sum1)                     #除以用户数目，指整个时间戳下，平均每个用户的误差
    return mae


def MAE2(Zall, originals, ti):  # 传入的是这个时间戳的真值(一维列表）和原始值（二维列表，包含用户数和观测数），还有时间戳
    objects = len(Zall[ti])  # 计算被观测点的数量
    sum1 = []  # 是一个一维数组
    mae = 0  # 初值为0
    Zti = Zall[ti]  # Zti表示t=i时间戳上，所有objects的真值

    truth= 0
    truthlist =[]
    truthlist[:] = []       #初始化为空
    # 下面对originals进行真值发现
    for object in range(objects):
        truth = 0
        for user in range(len(originals)):  # 求出用户个数
            truth = originals[user][object] +truth
        truth = truth/len(originals)
        truthlist.append(truth)

    # 对每个用户的观测的单个值进行计算，然后需要计算每个用户在每个观测点的误差范围
    user_devite = 0
    for obj in range(objects):  # 观测值数目
        user_devite = abs(truthlist[obj] - float(Zti[obj])) + user_devite  # 把每一个object对应的误差值放到sum1中
    user_devite = user_devite/objects          #先注释掉，因为目前这个单个用户误差并不太大          #除以objects的数目，指对于单个用户而言，它的误差是多少
    sum1.append(user_devite)
    sumall = 0
    for sumall in sum1:
        mae = sumall + mae
    mae = mae / len(sum1)  # 除以用户数目，指整个时间戳下，平均每个用户的误差
    return mae


def MAPE(Zall,originals,ti):  # 传入的是这个时间戳的真值(一维列表）和原始值（二维列表，包含用户数和观测数），还有时间戳；
    # mape,是每次计算的时候相对于原数据的误差

    objects = len(Zall[ti])  # 计算被观测点的数量
    sum1 = []
    mape = 0
    Zti = Zall[ti]  # Zti表示t=i时间戳上，所有objects的真值
    #print("second:",ti)
    # 对每个用户的观测的单个值进行计算，然后需要计算每个用户在每个观测点的误差范围
    for num in range(len(originals)):       #用户数目
        # for obj in range(objects):          #objects数目
        #     sum1.append(abs((originals[num][obj] - Zti[obj])/originals[num][obj]))
        user_devite = 0  # 初始的对于单个user，所有的object的误差和
        for obj in range(objects):  # 观测值数目
            user_devite = abs((originals[num][obj] - Zti[obj])/originals[num][obj])  # 把每一个object对应的误差值放到sum1中
        #user_devite = user_devite / objects  # 除以objects的数目，指对于单个用户而言，它的误差是多少
        sum1.append(user_devite)
    for sumall in sum1:
        mape = sumall + mape
    mape = mape / len(sum1)         #除以用户数目，指整个时间戳下，平均每个用户的误差
    return  mape


def MAPE2(Zall,originals,ti):  # 传入的是这个时间戳的真值(一维列表）和原始值（二维列表，包含用户数和观测数），还有时间戳；
    # mape,是每次计算的时候相对于原数据的误差

    objects = len(Zall[ti])  # 计算被观测点的数量
    sum1 = []
    mape = 0
    Zti = Zall[ti]  # Zti表示t=i时间戳上，所有objects的真值

    truth= 0
    truthlist =[]
    truthlist[:] = []       #初始化为空
    # 下面对originals进行真值发现
    for object in range(objects):
        truth = 0
        for user in range(len(originals)):  # 求出用户个数
            truth = originals[user][object] +truth
        truth = truth/len(originals)
        truthlist.append(truth)

    # 对每个用户的观测的单个值进行计算，然后需要计算每个用户在每个观测点的误差范围
    user_devite = 0  # 初始的对于单个user，所有的object的误差和
    for obj in range(objects):  # 观测值数目
        user_devite = abs((truthlist[obj] - float(Zti[obj]))/truthlist[obj]) + user_devite  # 把每一个object对应的误差值放到sum1中
    #user_devite = user_devite / objects  # 除以objects的数目，指对于单个用户而言，它的误差是多少
    sum1.append(user_devite)
    sumall = 0
    for sumall in sum1:
        mape = sumall + mape
    mape = mape / len(sum1)         #除以用户数目，指整个时间戳下，平均每个用户的误差
    return  mape


# list1=[[1,2],2,3,4,5,6]
# for i in range(len(list1)):
#     list1[i]=list1[i]
# print(list1)
# print(list1[0][1])