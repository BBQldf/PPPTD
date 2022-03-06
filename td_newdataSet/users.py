import numpy as np
import matplotlib.pyplot as plt
import math
import sympy
from txt_readin import Twodimension_Init

def PrivacyLevelConfirmation(k, rate):            #最开始的根据用户隐私级别的budget分割
    x1 = 0
    x2 = 1
    x = sympy.Symbol('x')
    t = sympy.Symbol('t')
    f = k*sympy.E**(-k*x)
    #f1 = sympy.integrate(f, (x, x1, t))/sympy.integrate(f, (x, x1, x2))-(1-rate)
    f1 = sympy.integrate(f, (x, x1, t)) / sympy.integrate(f, (x, x1, x2)) - (1 - rate)
    return sympy.solve(f1)[0]

# A=PrivacyLevelConfirmation(0.5, 0.5)
# B=PrivacyLevelConfirmation(0.5, 0.10)       # k值越大，A/B的值越小,会小于0.5；大概在rate=0.5的时候很接近，在rate=1的时候大概是0.45；
# print(A,B,A/B)

#epsilon=[]               #epsilon是用户端传上来的，也需要维护一个表吧？每一个用户对应着一个epsilon，同时也有时间标签，所以是一个和weight一样的二维数组

def perturbation(epsilon, originals, ti):        #三个参数：epsilon是对应用于加噪的参量，ti是当前时间戳
    xi = Twodimension_Init(50, 4, 0.0001)          #xi的初始化——16个users、26个objects，初值为0.0001
    for user in range(len(originals)):                      #originals是在某一时间戳下用户的原始数据，是个二维数组，有多用户多object；
        for obj in range(len(originals[0])):                 #对同一个用户而言，它对应的观测量objects的加噪是   不一样的!!!
            xi[user][obj] = originals[user][obj] + np.random.laplace(0., epsilon[ti][user][obj], 1)
                                #加噪
    return xi               #user端只需要返回一个加噪后的数据即可

