import sympy
import math

alpha=0.54
beta = 0.37             #关于隐私分配的用户调查模型

def PrivacyLevelConfirmation1(theta,rate):            #最开始的根据用户隐私级别的budget分割
    x1 = -3*theta
    x2 = 3*theta            #在[-3*theta,3*theta]之间包含了整个高斯分布
    Mu = 0
    x = sympy.Symbol('x')
    t = sympy.Symbol('t')
    #f = k*sympy.E**(-k*x)
    f =(1/(theta*sympy.sqrt(2*math.pi)))*sympy.E**-((x-Mu)*(x-Mu)/(2*theta*theta))
    #f1 = sympy.integrate(f, (x, x1, t))/sympy.integrate(f, (x, x1, x2))-(1-rate)
    f1 = sympy.integrate(f, (x, x1, t)) / sympy.integrate(f, (x, x1, x2)) - (1 - rate)
    # f2 = sympy.integrate(f, (x, x1, 1))
    # print(float(f2))
    return sympy.solve(f1)[0]

# y1 = PrivacyLevelConfirmation1(10,1-alpha-beta)            #theta越大，达到预期比重对应的x的值越大
# y2 = PrivacyLevelConfirmation1(10,1-alpha)
# print(y1,y2)


def PrivacyLevelConfirmation(k, rate):            #最开始的根据用户隐私级别的budget分割
    x1 = 0
    x2 = 1
    x = sympy.Symbol('x')
    t = sympy.Symbol('t')
    f = k*sympy.E**(-k*x)
    f1 = sympy.integrate(f, (x, x1, t))/sympy.integrate(f, (x, x1, x2))-(1-rate)
    return sympy.solve(f1)[0]


# A=PrivacyLevelConfirmation(1, rate=1-alpha)
# B=PrivacyLevelConfirmation(1, rate=1-alpha-beta)       # k值越大，A/B的值越小，最小为0.5；
# print(A,B,A/B)


scores = {'1': [89], '2': [92], '3': [93],4:[]}

scores['1'].append(22)
id = 5
for id in scores.keys():
    scores[id].append(22)
    print("sssss")

    #scores[5] = []

print(scores)