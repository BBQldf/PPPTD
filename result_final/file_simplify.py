# 尝试读取文件，对数据集进行初步处理，然后思路：
# 1、首先按时间戳，对每个大时间点下先分开；
# 2、对每个被监测点而言，尽量选择那些具备多个监测点的（这样可以保证监测点是相同的）
# 3、这个时候文件中的信息应该只有检测者（用户）id，被检测者的属性值（温度、光照、湿度、噪声等）
# 考虑一下这个时候真值发现的问题：算法应该是没有变哈德，因为我们是用户级的，只要保证参与实验的用户不再发生变化即可。
# 我们需要对scale重新设置，sensitivity需要用列表来存储；
# 而且高隐私用户和中隐私用户的界限也是通过列表来区分，但是这个是的epsilon的总值还是取第一个值，然后对不同的sensitivity，分配到不同的值；
#
import linecache
import os

# 选取原始文件中，时间戳是 "2004-03-06"，有两个观测点没有值，但是不影响，做第一步化简
# with open('./data.txt','r',encoding='utf-8') as f :
#     line = f.readline()         #读取一行文件，包括换行符
#     #line = line[:-1]       #去掉换行符
#     moteid = line.split()[3]
#     while line:
#
#         with open('./result/result_'+moteid+'.txt','a+',encoding='utf-8') as f_number:
#                 f_number.write(line)
#
#         line =f.readline()
#         moteid = line.split()[3]
# print(line)
# line = line[:-1]
# print(type(line))
#
# #读取54个文件，每个中的100个数据，做第二步化简
# path = "./result52/"  # 指定需要读取文件的目录
# files = os.listdir(path)  # 采用listdir来读取所有文件
# #files.sort()
#
# for file_ in files:  # 循环读取每个文件名
#     with open(path + file_, 'r') as file_obj:
#         print(file_)
#         lines = file_obj.readlines()
#         for line in lines[0:100]:
#             items = ''
#             for item in line.split()[4:8]:
#                 items = items+item +' '
#             with open('./result/'+file_, 'a+', encoding='utf-8') as f_object:
#                 f_object.write(items+'\n')
#
#
# 改文件名，pass
# list1 = os.listdir('./result52/')
# list1.sort()
#
# for num in range(1,54):
#     str1 = 'result_' +str(num) +'.txt'
#     print(str1)
#     print(list1[2],type(list1[2]))
#     if str1 in list1:
#         os.rename('./result52/'+str1,'./result52/'+'result_'+str(num)+'.txt')


# 规范化命名--将那些没有的number填补

# list1 = os.listdir('./result/')
# list1.sort()
# num =0
#
# for file in list1:
#     if num >= 30:
#         os.rename('./result/'+file,'./result/'+'result100_'+str(num-1)+'.txt')
#     num +=1

#
# list1 = os.listdir('./result/')
# list1.sort()
# for num in range(1,52):
#     name = 'result_' + str(num) + '.txt'
#     if name in list1:
#         with open('./result/' + name, 'r+', encoding='utf-8') as f_number:
#             line = f_number.readline()
#             data = line.split()[0]
#             while line:
#                 data = line.split()[0]
#                 with open('./result_data_num/' + str(data) +'_'+ str(num-1) + '.txt', 'a+', encoding='utf-8') as f_data_number:
#                     f_data_number.write(line)
#
#                 line = f_number.readline()


# 在每个文件中存储了每个时间戳下51个用户各自的100个观测值
# list1 = os.listdir('./result_data_num/')
# list1.sort()
#
#
# for data in range(3,28):
#     iterate_num = 1
#     while iterate_num <=6:
#         line_all = ''
#         for num in range(0,51):
#             if num != 4:
#                 name = '2004-03-02_' + str(num) + '.txt'
#                 if name in list1:
#                     line100 = ''
#                     line_index = 1
#                     while line_index <= 100:
#                         with open('./result_data_num/' + name, 'r+', encoding='utf-8') as f_number:
#                             line100 = line100 + linecache.getline('./result_data_num/'+name, line_index+iterate_num*100, module_globals=None)     #这个索引是从1开始的，和在文件中的基础索引一致
#                             line_index +=1
#             line_all = line_all +line100
#         with open('./result_user_task/' + '2004-03-'+'%02d'%data+'_' + str(iterate_num)+ '.txt', 'a+', encoding='utf-8') as f_timer:
#             f_timer.write(line_all)
#
#         iterate_num += 1


#选择需要的数据量——温度、湿度、光照、电压
# list1 = os.listdir('./result_user_task/')
# list1.sort()
# num =0
# for file in list1:
#     row100 = ''
#     with open('./result_user_task/' + file, 'r+', encoding='utf-8') as f_number:
#         for line_index in range(1, 101):  # 100个用户转化为100行
#             column51 = ''
#             for column in range(0, 50):  # 51个观测点转化为51列----只需索引到4900，所以边界是50
#                 data = linecache.getline('./result_user_task/' + file, line_index + column * 100, module_globals=None)
#                 data = data.strip().split(' ')[-1]
#                 #print(data)
#                 column51 = column51 + data + " "
#             row100 = row100 + column51 + '\n'
#
#     with open('./result_final/result_' + str(num) + '.txt', 'w+', encoding='utf-8') as f_final:
#         f_final.write(row100)
#     num += 1