
import os

with open('./result_final/result_78.txt', 'r+', encoding='utf-8') as f_24:
    lines = f_24.readlines()
    for line in lines:
        #line.replace('\\t',' ')
        datas =line.split('\t')
        newdata = ''
        num =0
        for data in datas:
            if num ==49:
                newdata =newdata +data
            else:
                newdata = newdata +data +' '
                num +=1
        with open('./result_final/result_78_2.txt', 'a+', encoding='utf-8') as f_24_2:
            f_24_2.write(newdata)