# -*- coding: utf-8 -*-
import matplotlib
matplotlib.rcParams['backend'] = 'SVG'
import matplotlib.pyplot as plt




# name_list = ['Weather','Inter Lab data']
# num_list = [2.0078,15.783]
# num_list1 = [1.8876,14.62]
# x = list(range(len(num_list)))
# x_tick = list(range(len(num_list)))     #x标签位置
# total_width, n = 0.8, 2
# width = total_width / n -0.2
#
# plt.bar(x, num_list, width=width, label='PPPTD', color='silver',edgecolor='black',hatch='\\\\')
# for i in range(len(x)):
#     x[i] = x[i] + width
#     x_tick[i] = x_tick[i] + width - 0.1
# plt.xticks(x_tick, name_list)
# plt.bar(x, num_list1, width=width, label='PPPTD w/o IAA',color='white', edgecolor='black',hatch='//')
# plt.legend()
# plt.ylabel('runtime(s)',fontsize=14)
# plt.show()
# plt.savefig('PPPTD wo IAA2.pdf', bbox_inches='tight')


name_list = ['Weather','Inter Lab data']
num_list = [2.0078,15.783]
num_list1 = [1.7986,13.96]
x = list(range(len(num_list)))
x_tick = list(range(len(num_list)))     #x标签位置
total_width, n = 0.8, 2
width = total_width / n -0.2

plt.bar(x, num_list, width=width, label='PPPTD', color='silver',edgecolor='black',hatch='\\\\')
for i in range(len(x)):
    x[i] = x[i] + width
    x_tick[i] = x_tick[i] + width - 0.1
plt.xticks(x_tick,name_list)
plt.bar(x, num_list1, width=width, label='PPPTD w/o IAA',color='white', edgecolor='black',hatch='//')
plt.legend()

plt.ylabel('runtime(s)',fontsize=14)
plt.show()
plt.savefig('PPPTD wo DWA2.pdf', bbox_inches='tight')