#server端的任务相对简单，只需要收集users的数据，然后处理
#但是需要server对每次的weight的值建一个表，因为我们需要每次都更新weight，并且求Wti的变化量，来确定什么时候更新budget
#然后后续还需要画图，所以还要对truth的值


import math
import random
import numpy as np
from copy import deepcopy


gamma = 1
rho=1000         #是动态budget调整中需要用到的一个参数;3是对应每4个间隔更新；5是对应每5个间隔更新;14对应6个间隔更新,30对应7个间隔
w=[]            #表示时间戳中，所有用户对应的weight，是一个二维数组
K=16     #用户数量，这里先这样表示，最后直接换成具体实数
#scale=[]               #epsiono是用户端传上来的，也需要维护一个表吧？每一个用户对应着一个epsiono，同时也有时间标签，所以是一个和weight一样的二维数组
newtime = -1        #新的更新时间，
#newuser= []                    # 需要更新的用户id，是一个一维数组，因为需要更新的用户
objectaita = [3.2,8]            #可调整的epsiono的阈值
PI=0.1       #预设的一个epsiono值
newepsiono = 0         #是一个值，对应着每个object的更新的那个值
sensitivity = 5
maxepsiono = 8




def adaptive_sample(tilast , tj,scale,w,epsionolist,adaptive_user):  # 传入：两个参数上一个更新点的时间和当前时间点
    global  K,rho,newtime,newepsiono,sensitivity,maxepsiono,objectaita
    objectaita[0] = epsionolist[1] - 0.05
    newuser = []  # 需要更新的用户id，是一个一维数组，因为需要更新的用户
    newuser[:] = []                 #初始化为空

    pending_user = []               #记录总的detaW > 0的用户id，作为待定更新用户
    pending_user[:] = []                 #初始化为空
    pending_user1 = []               #记录detaW > 0的用户id，作为待定更新用户
    pending_user1[:] = []                 #初始化为空
    pending_user_detaW = {}             #记录每一个用户，它的所有detaW的更新值，用于求最后的总的detaW是否大于0


    #下面构造每一用户模型下的隐私分配
    # sensitivity1aita= []
    # sensitivity1 = np.array(sensitivity)
    # sensitivity1aita.append((sensitivity1 / objectaita[0]).tolist())
    # sensitivity1aita.append((sensitivity1 / objectaita[1]).tolist())

    for time1 in range(1,tj - tilast+1):       #从ti开始遍历，到tj-1，time1表示的就是detaT(time是关键字），
                #间隔时间从1开始到tj-tilast，为了防止在最开始的更新点ti=0时，计算w[tilast+time1-1]出错
        for userid in range(len(w[0])):         #对于每一个用户而言，都需要做一次判断，是否需要更新epsiono
            # sensitivity2 = np.array(sensitivity)
            # sensitivity2max = sensitivity2/maxepsiono
            # sensitivity2max = sensitivity2max.tolist()      #处理list不能直接除int型变量的问题
            if scale[tilast+time1][userid][0] == sensitivity/maxepsiono :        #不对低隐私用户进行更新;对应低隐私用户而言，他的每一个object都是5/8，这个是不变的，所以可以拿来直接做判断
                continue        #跳过
            else:                       #高、中隐私用户更新判断
                detaW = w[tilast+time1][userid] /sumW(w[tilast+time1]) - w[tilast+time1-1][userid] / sumW(w[tilast+time1-1])  # 这里计算Ti的weight和Ti-1的权重变化
                # if detaW > 0:              #如果用户的权值变化是非正的话，意味着这个用户权值比重相较于前一时刻在减小，说明用户是不“重要的”，就不更新
                #     #if abs(detaW) > (math.sqrt(scale[tilast+time1][userid])/K):
                #     if abs(detaW) > (math.sqrt(Epsiono) / K):           #这里换成大写的epsiono是表示这是一个固定值
                #         newtime = time1 + tilast
                #         newuser = userid
                #     elif (time1-1) * (time1 - 2)*(2 * (time1) - 3) * Epsiono / 6 > rho:               #间隔时间1、2，都是0.设计的很巧妙，意思说不用考虑这段时间的累积误差了
                #         newtime = time1 + tilast
                #         newuser = userid
                #     else:
                #         newtime = tilast
                # else:                   #如果不是更新点，newtime还是等于上一个更新时间点
                #     newtime = tilast
                if detaW > 0:                           #统计每小段时间内，detaW大于0的用户id，把这个作为后续一长段时间来如果需要更新的用户；使用list.count函数，选择那些出现次数是整个一长段的时间差的userid
                    pending_user1.append(userid)
                #     if userid in pending_user_detaW.keys():         #如果这个用户之前已经存在在元组中，就将新的detaW放到其中
                #         pending_user_detaW[userid].append(detaW)
                #     else:                                           #没有这个用户就创建一个新的
                #         pending_user_detaW[userid] = [detaW]

                if userid not in pending_user:
                    pending_user.append(userid)

                if userid in pending_user_detaW.keys():         #如果这个用户之前已经存在在元组中，就将新的detaW放到其中
                    pending_user_detaW[userid].append(detaW)
                else:                                           #没有这个用户就创建一个新的
                    pending_user_detaW[userid] = [detaW]

                if abs(detaW) > (math.sqrt(PI) / K):  # 这里换成大写的epsiono是表示这是一个固定值
                    newtime = time1 + tilast
                    newuser.append(userid)

        if newuser :             #说明有用户需要更新
            print("detaW:",newuser)
            #print(len(newuser))
            scale, tilast,adaptive_user = Choosen_Time_Users(newtime, newuser, scale, tj,adaptive_user)  # 对更新时间点newtime上的需要更新的用户newuser的每一个object都更新
        elif (time1 - 1) * (time1 - 2) * (2 * (time1) - 3) * PI / 6 > rho:  # 间隔时间1、2，都是0.设计的很巧妙，意思说不用考虑这段时间的累积误差了
            newtime = time1 + tilast
            print("pendinguser_detaW:",pending_user_detaW)
            newuser1 = Figureout_Users(pending_user1,tilast,tj)
            print("newuser1:",newuser1)
            newuser2 = Figureout_Users2(pending_user, pending_user_detaW)
            print("newuser2:",newuser2)
            newuser = Figureout_Users_final(newuser1,newuser2)
            print("newuser_final:",newuser)
            print("ti:",tilast,";tj:",tj)           #上一个更新点，和这一时刻更新点
            print("detaT:",time1)               #间隔时间，这是一个固定值
            print("detaT_pendinguser:", pending_user)       #候选用户
            #print("detaT_newuser:",newuser)          #更新用户

            scale, tilast,adaptive_user = Choosen_Time_Users(newtime, newuser, scale, tj,adaptive_user)
        else:                       #不更新
            newtime = tilast

            # if newtime != tilast :            # 如果需要更新，那我们需要调整新的epsiono,而且是只对需要调整的用户做调整，所以还要维护一个需要调整的用户列表
            #     scale, tilast = Choosen_Time_Users(newtime, newuser, scale, tj)          #对更新时间点newtime上的需要更新的用户newuser的每一个object都更新
                # for object in range(len(scale[tilast][newuser])):     #对于每一个用户的多个objects而言：
                #     #newepsiono = scale[tilast+time1][newuser][object]          #ti时间戳里面的需要更新的用户对应的epsiono值
                #     newepsiono = scale[tj+1][newuser][object]             #我要更新的是下一个时间点，扰动的数据
                #     #newepsiono = apdate_epxiono(newepsiono)            #产生新的epsiono
                #     #这里需要区分一下，怎么把两个区间分开；并且是对整个用户；可以考虑直接用两个列表，都是除以maxepsiono之后的
                #     if newepsiono > sensitivity1aita[1][object] and newepsiono < sensitivity1aita[0][object]:  #表示这是中隐私              # 所以server还需要保存两个隐私预算的范围
                #         newepsiono = apdate_scale(newepsiono)  # 产生新的epsiono
                #         if newepsiono < sensitivity1aita[1][object]:        #新的sensitivity/epsiono小于低隐私的阈值
                #             newepsiono = sensitivity1aita[1][object]
                #     else:                   #表示这是高隐私用户
                #         newepsiono = apdate_scale(newepsiono)  # 产生新的epsiono
                #         if newepsiono < sensitivity1aita[0][object]:  # 新的sensitivity/epsiono小于中隐私的阈值
                #             newepsiono = sensitivity1aita[0][object]
                #
                #     scale[tj+1][newuser][object]=newepsiono           #我要更新的是下一个时间点，扰动的数据
                # tilast=newtime
                # print("userid:",newuser)
                # return scale,tilast               #当出现更新的时候我们程序就可以返回了——更新后的epsiono列表和最新的更新点
        #print("新的更新点：",tilast)

    return scale, tilast ,objectaita,adaptive_user     #对于不更新的情况，也要返回

    #考虑一下低隐私权重不再更新的情况

def sumW(w):            #求某一时间t所有用户的权值总和
    usersweight=0
    for weight in range(len(w)):
        usersweight = usersweight + w[weight]
    return usersweight                      #返回总的权值之和

def apdate_scale1(scale):
    newepsiono = random.uniform(0.66,0.90)*scale
    return newepsiono

def apdate_scale(scale):
    global gamma,sensitivity

    newepsiono =  sensitivity/scale +gamma
    newscale = sensitivity / newepsiono

    return newscale




def Figureout_Users(pending_user,tilast,tj):                #从待选用户中找出最后更新的用户
    adapteuser = []
    adapteuser[:] = []
    for x in pending_user :
        if pending_user.count(x) >= (tj-tilast)/2 :
            if not x in adapteuser:
                adapteuser.append(x)            #这些这段时间里面detaW都大于0的用户id
    return adapteuser


def Figureout_Users2(pending_user,pending_user_detaW):                #从待选用户中找出最后更新的用户
    adapteuser = []
    adapteuser[:] = []
    SumDetaW = 0
    for userid in pending_user:
        for detaW in pending_user_detaW[userid]:
            SumDetaW += detaW
        if SumDetaW > 0 :
            adapteuser.append(userid)
    return adapteuser



def Figureout_Users_final(newuser1,newuser2):
    newuser_final = []
    newuser_final[:] = []
    for user in newuser1:
        if user in newuser2:
            newuser_final.append(user)

    return newuser_final


def Choosen_Time_Users(newtime,newusers,scale,tj,adaptive_user):              #更新这一时间点上的部分用户的scale
    global sensitivity,objectaita      #引用上面的敏感度和最大的epsiono值

    #下面构造每一用户模型下的隐私分配
    scaleaita= []
    scaleaita[:] = []       #初始化为空
    scaleaita.append(sensitivity / objectaita[0])       #这个是高隐私的边界——5/4
    scaleaita.append(sensitivity / objectaita[1])       #这个是中隐私的边界——5/8
    for newuser in newusers:                #取列表中的用户id
        # newscale = scale[tilast+time1][newuser][object]          #ti时间戳里面的需要更新的用户对应的epsiono值
        #newscale = scale[tj + 1][newuser][object]  # 我要更新的是下一个时间点，扰动的数据
        #上面的不对，我要更新的是从这个时间点之后的所有时间，是一段时间，要用for循环
        newscale = scale[tj][newuser][0]
        # 这里需要区分一下，怎么把两个区间分开；并且是对整个用户；可以考虑直接用两个列表，都是除以maxepsiono之后的
        if newscale > scaleaita[1] and newscale < scaleaita[0]:  # 表示这是中隐私              # 所以server还需要保存两个隐私预算的范围
            newscale = apdate_scale(newscale)  # 产生新的scale
            if newscale < scaleaita[1]:  # 新的sensitivity/epsiono小于低隐私的阈值
                newscale = scaleaita[1]
                adaptive_user +=1
        elif newscale > scaleaita[0] :  # 表示这是高隐私用户
            newscale = apdate_scale(newscale)  # 产生新的scale
            if newscale < scaleaita[0]:  # 新的sensitivity/epsiono小于中隐私的阈值
                newscale = scaleaita[0]
                adaptive_user +=1
        #scale[tj + 1][newuser][object] = newscale  # 我要更新的是下一个时间点，扰动的数据
        for object in range(len(scale[newtime][newuser])):  # 对于每一个用户的多个objects而言：
            scale[tj][newuser][object] = newscale
        print("userid:", newuser)
    tilast = newtime
    return scale, tilast,adaptive_user  # 当出现更新的时候我们程序就可以返回了——更新后的epsiono列表和最新的更新点


#ztj=[]     #ztj表示在时间t时刻，object=j的真值,最后将所有的object的值都放在ztj中




def Weight_Computation(xi,ti,scale,w,Zall):     #weight估计;需要用户上传的数据xi——表示t=i的时间里面所有用户对所有任务上传的数据（加噪后），是一个二维数组
    sumwti=sumW(w[ti])                      #ti表示当前的时间戳
    #Zall = []  # Zall表示所有时刻的真值
    ztj = []                                      #epsiono是后面用于更新weight值
    ztj[:] = []                         #每次更新之后，要清空上一次的真值序列

    #下面求每个object对应的真值
    for j in range(len(xi[0])):          #这里求object的数目
        xij = 0  # xij表示所有用户对object的扰动值乘以对应的weight
        for i in range(len(xi)):      #二维数组xi，对应直接求的len即为其行数，表示用户数目
            xij=xi[i][j] * w[ti][i] +xij        #一个for循环做完就是关于object=j的任务求得的扰动值
        ztj.append(xij/sumwti)      #加权扰动值，即真值
    ztj = deepcopy(ztj)
    Zall.append(ztj)        #每个时间都要加入列表中

    #接着求这个时间点上，所有用户到真值的距离之和，以及所有用户对应的epsiono之和

    sumLti=[]               #记录每一个用户到真值的距离
    sumallLti = 0           #记录所有用户到真值的距离和
    sumLti[:] = []
    for i in range(len(xi)):         #表示用户id
        Lti = 0      #某一个用户i的上传值和真实值的距离
        for j in range(len(xi[0])):          #遍历每一个object
            Lti = math.pow(xi[i][j]-ztj[j],2)+Lti
        sumLti.append(Lti)              #记录每一个用户到真值的距离
    sumallLti=sumW(sumLti)          #计算所有的距离和

    # sumepsiono = 0    #记录所有用户的、所有任务的scale之和
    # for user in range(len(xi)):
    #     sumepsiono = sumW(scale[ti][user]) + sumepsiono

    epsionoall = []             #每次在weight_computation函数中重新计算总的epsiono值
    epsionoall[:] = []      #初始化为空；由于每次的scale[tj][userid][0]代表了这个时间戳下这个用户的scale（单个用户有多个obj，但是scale都一样）
    for user in range(len(xi)):      #二维数组xi，对应直接求的len即为其行数，表示用户数目
        epsionoall.append(5/scale[ti][user][0])

    #计算所有用户的epsiono值
    sumepsiono = sumW(epsionoall)               #这里还是要用sensitivity/scale[ti][user][0],所以要传入保存的epsionall，
                                        # 但是还没有记录更新的epsionoall。待改进
    print("用户的总epsiono值为：",sumepsiono)
    with open('.//data//sumepsiono.txt', 'a+', encoding='utf-8') as f:
        f.write(str(sumepsiono)+'\n')

#下面求对每个用户调整的weight
    for i in range(len(xi)):             #表示用户id
        w[ti+1][i] = -math.log((sumLti[i]/sumallLti)*math.log(3-(epsionoall[i]/sumepsiono),2),2) #这个是对下一个时间戳的weight调整
        #w[ti+1][i] = -math.log(sumLti[i]/sumallLti,2)      #第二种更新方案
    return Zall , sumepsiono



def Weight_Computation1(xi,ti,scale,wwe,Zallwe):     #weight估计;需要用户上传的数据xi——表示t=i的时间里面所有用户对所有任务上传的数据（加噪后），是一个二维数组
    sumwti=sumW(wwe[ti])                      #ti表示当前的时间戳
    ztj = []                                        #epsiono是后面用于更新weight值
    ztj[:] = []                         #每次更新之后，要清空上一次的真值序列
    #下面求每个object对应的真值
    for j in range(len(xi[0])):          #这里求object的数目
        xij = 0  # xij表示所有用户对object的扰动值乘以对应的weight
        for i in range(len(xi)):      #二维数组xi，对应直接求的len即为其行数，表示用户数目
            xij=xi[i][j] * wwe[ti][i] +xij        #一个for循环做完就是关于object=j的任务求得的扰动值
        ztj.append(xij/sumwti)      #加权扰动值，即真值
    ztj = deepcopy(ztj)
    Zallwe.append(ztj)        #每个时间都要加入列表中

    #接着求这个时间点上，所有用户到真值的距离之和，以及所有用户对应的epsiono之和
    sumLti=[]               #记录每一个用户到真值的距离
    sumallLti = 0           #记录所有用户到真值的距离和
    sumLti[:] = []
    for i in range(len(xi)):         #表示用户id
        Lti = 0      #某一个用户i的上传值和真实值的距离
        for j in range(len(xi[0])):          #遍历每一个object
            Lti = math.pow(xi[i][j]-ztj[j],2)+Lti
        sumLti.append(Lti)              #记录每一个用户到真值的距离
    sumallLti=sumW(sumLti)          #计算所有的距离和

    # sumepsiono = 0    #记录所有用户的、所有任务的epsiono之和
    # for user in range(len(xi)):
    #     sumepsiono = sumW(scale[ti][user]) + sumepsiono
    epsionoall = []             #每次在weight_computation函数中重新计算总的epsiono值
    epsionoall[:] = []      #初始化为空；由于每次的scale[tj][userid][0]代表了这个时间戳下这个用户的scale（单个用户有多个obj，但是scale都一样）
    for user in range(len(xi)):      #二维数组xi，对应直接求的len即为其行数，表示用户数目
        epsionoall.append(5/scale[ti][user][0])

    #计算所有用户的epsiono值
    sumepsiono = sumW(epsionoall)               #这里还是要用sensitivity/scale[ti][user][0],所以要传入保存的epsionall，
                                        # 但是还没有记录更新的epsionoall。待改进
    print("用户的总epsiono值为：",sumepsiono)

#下面求对每个用户调整的weight
    for i in range(len(xi)):             #表示用户id
        #w[ti+1][i] = -math.log((sumLti[i]/sumallLti)*math.log(3-(sumW(scale[ti][i])/sumepsiono),2),2) #这个是对下一个时间戳的weight调整
        wwe[ti+1][i] = -math.log(sumLti[i]/sumallLti,2)      #第二种更新方案
    return Zallwe,sumepsiono