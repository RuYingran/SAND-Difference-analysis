import numpy as np
import itertools
import random
from concurrent.futures import ProcessPoolExecutor
BIT=32
WINDOWS=6
#ROUND=7
S=[['00'],['11','13','91','93'],['22','24','26','a2','a4','a6'],['31','33','37','b1','b3','b5'],['44','46','54','56','d4','d6'],['45','47','55','57','d5','d7'],['66','72','e4','f2'],['61','63','75','77','e1','e3','f5','f7'],['1c','1e','88','8c','8e','98'],['1d','1f','8b','8d','8f','99'],['2a','2c','3a','3e','aa','ae','ba','bc'],['29','2d','3b','3d','a9','af','bb','bf'],['58','c8','cc','ce','dc','de'],['5b','c9','cd','cf','dd','df'],['6a','6c','7a','7c','ea','ee','fa','fe'],['6b','6f','79','7d','eb','ed','f9','ff']]
S_prob=[[0],[2,2,2,2],[2,3,3,2,3,3],[3,3,2,3,3,2],[2,2,3,3,3,3],[2,2,3,3,3,3],[2,2,2,2],[3,3,3,3,3,3,3,3],[3,3,2,3,3,2],[3,3,2,3,3,2],[3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3],[2,2,3,3,3,3],[2,2,3,3,3,3],[3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3]]

def int_to_bin32(x):
    binary_str = bin(x & 0xFFFFFFFF)[2:].zfill(32)  # 将整数转换为32位二进制数的字符串
    binary_list = [int(bit) for bit in binary_str]
    return binary_list

def count_trailing_zeros(binary_num):
    count = 0
    for bit in reversed(binary_num):
        if bit == '0':
            count += 1
        else:
            break
    return count

def binary_array_to_int(binary_array):
    binary_str = ''.join([str(bit) for bit in binary_array])
    decimal_int = int(binary_str, 2)
    return decimal_int
def decimal_array_to_hex_eight_digits(int_array):
    hex_array = [hex(num)[2:].zfill(8) for num in int_array]
    return hex_array

def S_all(a):
    value=[]
    prob=[]
    total_value=[]
    total_prob=[0]
    for x in a:
        value.append(S[int(x,16)])
        prob.append(S_prob[int(x,16)])
    #print(value)
    #print(prob)
    N0_all=['']
    N1_all=['']
    for sub_list in value:
        N0_all=[x + str(hex((int(y,16)>>4))[2:]) for x in N0_all for y in sub_list]
        N1_all=[x + str(hex(int(y,16)&0xf)[2:]) for x in N1_all for y in sub_list]
    #print("N0",N0_all)
    #print("N1",N1_all)
    for i in range(0,len(N0_all)):
        total_value.append(hex(int(N0_all[i],16)^ROTL(int(N1_all[i],16),4))[2:].zfill(8))
    for sub_list in prob:
        total_prob=[x+y for x in total_prob for y in sub_list]
    #print(len(total_value))
    #print(len(total_prob))
    return total_value,total_prob

def ROTL(x, n):
    return ((x << n) | (x >> (32 - n))) & ((1 << 32) - 1)

def ROTR(x, n):
    return ((x >> n) | (x << (32 - n))) & ((1 << 32) - 1)


def P(x):
    return ROTL(x & 0x0F0F0F0F, 28) | ROTL(x & 0xF0F0F0F0, 12)

def P_inverse(x):
    return ROTR(x,28)&0x0F0F0F0F|ROTR(x,12)&0xF0F0F0F0


def hex_to_32bit_binary(value):
    value_bin=[]
    for x in value:
        value_bin.append(bin(int(x, 16))[2:].zfill(32))
    return value_bin

def count_zeros_in_list(lst):
    count_list = [0]*32  # 初始化一个包含32个零的列表，用于统计每个位置为0的个数
    for num in lst:
        for i, bit in enumerate(num):
            if bit == '0':
                count_list[i] += 1
    return count_list

def generate_all_possibilities(binary_str, positions):
    length = len(positions)
    possibilities = []
    
    for i in range(2**length):  # 生成所有可能的组合
        possibility = list(binary_str)
        for j in range(length):
            bit = (i >> j) & 1  # 检查第j位是0还是1
            possibility[positions[j]] = str(bit)  # 将指定位置设置为相应的值
        possibilities.append(''.join(possibility))
    
    return possibilities


def U_a(a):
    t_value=[]
    a=int(a,16)
    a_hex=[hex_digit for hex_digit in hex(a)[2:].zfill(8)]
    #print(a_hex)
    output_value,output_prob=S_all(a_hex)
    for x in output_value:
        t_value.append(hex(P(int(x,16)))[2:].zfill(8))
    return t_value,output_prob

#确定窗口W_l的BS和AC,这里在确定BS的时候是把概率最大的一个差分拿出来估计BS
def bs_ac(value,prob):
    #print(value)
    BS=''
    t_value=[]
    t_prob=[]
    #print(value)
    #取最大概率值的value
    max_prob=min(prob)
    for i in range(0,len(prob)):
        if prob[i]==max_prob:
            t_value.append(value[i]) #取出概率最大的输出差分和其概率
            t_prob.append(prob[i])
    t_value=hex_to_32bit_binary(t_value)
    #print(t_value)
    #print(t_prob)
    #统计每个位上0的个数
    length=len(t_value)
    #print(length)
    #原本的二进制要改成十六进制
    count_list=count_zeros_in_list(t_value)
    #print(count_list)
    AC=[]
    for i in range(0,len(count_list)):
        if count_list[i]==(length/2):
            if (len(AC)<=WINDOWS):
                AC.append(i)
    #print(AC)
    for i in range(0,len(count_list)):
        if count_list[i]==length:
            BS+='0'
            continue
        elif count_list[i]==0:
            BS+='1'
            if (len(AC)<WINDOWS):
                AC.append(i)
            continue
        else:
            BS+='0'#这个地方的索引号要保留，就是我们要找的AC
            continue
    #print(AC)
    while len(AC) < WINDOWS:
        num = random.randint(0, 31)
        if num not in AC:
            AC.append(num)
    #print("BS",hex(int(BS,2))[2:].zfill(8))
    #print("AC",AC)
    all_value_hex=[]
    all_value=generate_all_possibilities(BS,AC)
    for x in all_value:
        all_value_hex.append(hex(int(x,2))[2:].zfill(8))
    #print(all_value_hex)
    update_prob=[]
    update_value=[]
    #把所有可能的值都算出来了然后查找概率
    index_dict = {v: index for index, v in enumerate(value)}
    indices = [index_dict[v] for v in all_value_hex if v in index_dict]
    #print(indices)
    for i in range(0,len(indices)):
        update_value.append(value[indices[i]])
        update_prob.append(prob[indices[i]])
    return update_value,update_prob,AC
    
def check_diff(t_v,t_r,value,r,prob):
    temp=""
    for i in range(0,len(value)):
        if t_v==value[i]:
            if t_r==r[i]:
                temp=temp+"+"+str(prob[i])
    return t_v,t_r,temp

def diff(value,r,prob):
    total=list(zip(value,r))
    total=set(total)
    total=list(total)
    with ProcessPoolExecutor() as executor:  # 创建进程池
        futures = []
        for i in range(0, len(total),50):
            for j in range(50):
                if (i+j)<len(total):
                    #print("chuangzaojingcehng")
                    futures.append(executor.submit(check_diff, total[i+j][0], total[i+j][1], value,r,prob,))
        for future in futures:
            t_v, t_r, temp = future.result()
            print("左边结果",t_v)
            print("右边结果",t_r)
            print("差分概率",temp)
            print("\n")


def process_value(t_v, t_p, t_r):
    new_v = []
    new_prob = []
    new_r = []
    value, prob = U_a(t_v)
    value, prob, AC = bs_ac(value, prob)
    prob = [x + t_p for x in prob]
    for k in range(0, len(value)):
        value[k] = hex(int(value[k], 16) ^ int(t_r, 16))[2:].zfill(8)
        print(value[k])
        print(prob[k])
        print(t_v)
        print("\n")
        new_v.append(value[k])
        new_prob.append(prob[k])
        new_r.append(t_v)
    return new_v, new_r, new_prob


def F_S(t_value, t_prob, t_r):
    new_v_all = []
    new_prob_all = []
    new_r_all = []
    #factor=find_factors(len(t_value))
    with ProcessPoolExecutor() as executor:  # 创建进程池
        futures = []
        for i in range(0, len(t_value),50):
            for j in range(50):
                if (i+j)<len(t_value):
                    futures.append(executor.submit(process_value, t_value[i+j], t_prob[i+j], t_r[i+j],))
        for future in futures:
            new_v, new_r, new_prob = future.result()
            new_v_all.extend(new_v)
            new_prob_all.extend(new_prob)
            new_r_all.extend(new_r)

    f_v, f_r, f_p = new_v_all, new_r_all, new_prob_all
    return f_v, f_r, f_p


# 打开一个txt文件，如果不存在会自动创建
with open('output_1.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f

    value_0=[]
    prob_0=[]
    r_0=[]
    #第0轮
    a='09000890'
    r='88880230'
    value,prob=U_a(a)
    value,prob,AC=bs_ac(value,prob)
    for i in range(0,len(value)):
        #计算下一轮进入的输入差分即概率
        value[i]=hex(int(value[i],16)^int(r,16))[2:].zfill(8)
        value_0.append(value[i])
        prob_0.append(prob[i])
        r_0.append(a)
    #value_0,r_0,prob_0=diff(value_0,r_0,prob_0)
sys.stdout = sys.__stdout__
print("第1轮结束")

with open('output_2.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f

    r='09000890'
    #第1轮
    value_1=[]
    prob_1=[]
    r_1=[]
    for i in range(0,len(value_0)):
        value,prob=U_a(value_0[i])
        value,prob,AC=bs_ac(value,prob)
        prob=[x + prob_0[i] for x in prob]
        for j in range(0,len(value)):
        #计算下一轮进入的输入差分即概率
            value[j]=hex(int(value[j],16)^int(r,16))[2:].zfill(8)
            value_1.append(value[j])
            prob_1.append(prob[j])
            r_1.append(value_0[i])
    #value_1,r_1,prob_1=diff(value_1,r_1,prob_1)
sys.stdout = sys.__stdout__
print("第2轮结束")

with open('output_3.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f
    value_2,r_2,prob_2=F_S(value_1,prob_1,r_1)
    print(value_2)
    print(r_2)
    print(prob_2)
sys.stdout = sys.__stdout__
print("第3轮结束")

with open('output_4.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f
    value_3,r_3,prob_3=F_S(value_2,prob_2,r_2)
    print(value_3)
    print(r_3)
    print(prob_3)
sys.stdout = sys.__stdout__
print("第4轮结束")

with open('output_5.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f
    value_4,r_4,prob_4=F_S(value_3,prob_3,r_3)
    print(value_4)
    print(r_4)
    print(prob_4)
sys.stdout = sys.__stdout__
print("第5轮结束")

with open('output_6.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f
    value_5,r_5,prob_5=F_S(value_4,prob_4,r_4)
    print(value_5)
    print(r_5)
    print(prob_5)
sys.stdout = sys.__stdout__
print("第6轮结束")

t_left=[]
t_right=[]
temp_prob=[]
for i in range(len(value_5)):
    if prob_5[i]<=24:
        t_left.append(value_5[i])
        t_right.append(r_5[i])
        temp_prob.append(prob_5[i])
with open('7轮高概率差分特征.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f
    value_6,r_6,prob_6=F_S(t_left,temp_prob,t_right)
    for i in range(len(value_6)):
        print("左边结果",value_6[i])
        print("右边结果",r_6[i])
        print("概率",prob_6[i])
        print("\n")
sys.stdout = sys.__stdout__
print("第7轮结束")

#根据高概率差分特征头尾寻找高概率差分
tp1=[]
tp2=[]
tp3=[]
t1=[]
t2=[]
t3=[]
for i in range(len(value_5)):
    if value_5[i] in r_6:
        tp1.append(value_5[i])
        tp2.append(r_5[i])
        tp3.append(prob_5[i])
for i in range(len(tp1)):
    v,r,p=process_value(tp1[i],tp3[i],tp2[i])
    t1.extend(v)
    t2.extend(r)
    t3.extend(p)
with open('7轮高概率差分特征.txt', 'w') as f:
    # 重定向print输出到文件
    import sys
    sys.stdout = f
    diff(t1,t2,t3)
sys.stdout = sys.__stdout__

