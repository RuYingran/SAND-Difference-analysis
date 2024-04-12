import cplex
from cplex.exceptions import CplexError


Round=4
problem = cplex.Cplex()
x_number=576
a_number=16*Round
d_number=32*2*Round
problem.variables.add(names=["x{}".format(i) for i in range(1,x_number+1)], lb=[0] * x_number, ub=[1] * x_number, types=['B'] * x_number)
problem.variables.add(names=["a{}".format(i) for i in range(1,a_number+1)],lb=[0] * a_number, ub=[1] * a_number, types=['B'] * a_number)
problem.variables.add(names=["d{}".format(i) for i in range(1,d_number+1)],lb=[0] * d_number, ub=[1] * d_number, types=['B'] * d_number)

index=[]
for i in range(1,a_number+1):
    index.append(('a'+str(i),1))

problem.objective.set_linear(index)
problem.objective.set_sense(problem.objective.sense.minimize)

all_list=[]
for i in range(1,33):
    all_list.append('x'+str(i))
small_lists = [all_list[i:i+4] for i in range(0, len(all_list), 4)]
b_list=[]
for i in range(65,129):
    b_list.append('x'+str(i))
b_small=[b_list[i:i+4] for i in range(0, len(b_list), 4)]
count1=1
count2=0
#S盒
for temp in small_lists:
    t1=temp+b_small[count2]
    t2=temp+b_small[count2+1]
    t3=b_small[count2]+temp
    t4=b_small[count2+1]+temp
    problem.linear_constraints.add(lin_expr=[[t1, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t2, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t3, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t4, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    temp.pop()
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    count2+=2
#print(count1)
#异或
t1=[]
for i in range(65,129):
    t1.append('x'+str(i))
t1_lists = [t1[i:i+4] for i in range(0, len(t1), 4)]
t2=[]
for i in range(129,161):
    t2.append('x'+str(i))
t2_lists = [t2[i:i+4] for i in range(0, len(t2), 4)]
s1=[]
s2=[]
for i in range(len(t1_lists)):
    if i%2==0:
        s1.append(t1_lists[i])
    else:
        s2.append(t1_lists[i])
#print(s1)
temp=s2.pop(0)
s2.append(temp)
#print(s2)
count3=1
for i in range(0,len(s1)):
    for j in range(0,4):
        temp=[]
        temp.append(s1[i][j])
        temp.append(s2[i][j])
        temp.append(t2_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1

#移位
tt=[0]*8
tt[0]=t2_lists[7]
tt[1]=t2_lists[4]
tt[2]=t2_lists[1]
tt[3]=t2_lists[6]
tt[4]=t2_lists[3]
tt[5]=t2_lists[0]
tt[6]=t2_lists[5]
tt[7]=t2_lists[2]
#print(temp)

t3=[]
for i in range(33,65):
    t3.append('x'+str(i))
t3_lists = [t3[i:i+4] for i in range(0, len(t3), 4)]
#print(t3_lists)
t4=[]
for i in range(161,193):
    t4.append('x'+str(i))
t4_lists = [t4[i:i+4] for i in range(0, len(t4), 4)]

for i in range(0,len(tt)):
    for j in range(0,4):
        temp=[]
        temp.append(tt[i][j])
        temp.append(t3_lists[i][j])
        temp.append(t4_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1
#一轮结束

        
all_list=[]
for i in range(161,193):
    all_list.append('x'+str(i))
small_lists = [all_list[i:i+4] for i in range(0, len(all_list), 4)]
b_list=[]
for i in range(193,257):
    b_list.append('x'+str(i))
b_small=[b_list[i:i+4] for i in range(0, len(b_list), 4)]
count2=0
#S盒
for temp in small_lists:
    t1=temp+b_small[count2]
    t2=temp+b_small[count2+1]
    t3=b_small[count2]+temp
    t4=b_small[count2+1]+temp
    problem.linear_constraints.add(lin_expr=[[t1, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t2, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t3, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t4, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    temp.pop()
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    count2+=2
#print(count1)
#异或
t1=[]
for i in range(193,257):
    t1.append('x'+str(i))
t1_lists = [t1[i:i+4] for i in range(0, len(t1), 4)]
t2=[]
for i in range(257,289):
    t2.append('x'+str(i))
t2_lists = [t2[i:i+4] for i in range(0, len(t2), 4)]
s1=[]
s2=[]
for i in range(len(t1_lists)):
    if i%2==0:
        s1.append(t1_lists[i])
    else:
        s2.append(t1_lists[i])
#print(s1)
temp=s2.pop(0)
s2.append(temp)
#print(s2)
#count3=1
for i in range(0,len(s1)):
    for j in range(0,4):
        temp=[]
        temp.append(s1[i][j])
        temp.append(s2[i][j])
        temp.append(t2_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1

#移位
tt=[0]*8
tt[0]=t2_lists[7]
tt[1]=t2_lists[4]
tt[2]=t2_lists[1]
tt[3]=t2_lists[6]
tt[4]=t2_lists[3]
tt[5]=t2_lists[0]
tt[6]=t2_lists[5]
tt[7]=t2_lists[2]
#print(tt)

t3=[]
for i in range(1,33):
    t3.append('x'+str(i))
t3_lists = [t3[i:i+4] for i in range(0, len(t3), 4)]

t4=[]
for i in range(289,321):
    t4.append('x'+str(i))
t4_lists = [t4[i:i+4] for i in range(0, len(t4), 4)]

for i in range(0,len(tt)):
    for j in range(0,4):
        temp=[]
        temp.append(tt[i][j])
        temp.append(t3_lists[i][j])
        temp.append(t4_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1

#二轮结束

all_list=[]
for i in range(289,321):
    all_list.append('x'+str(i))
small_lists = [all_list[i:i+4] for i in range(0, len(all_list), 4)]
b_list=[]
for i in range(321,385):
    b_list.append('x'+str(i))
b_small=[b_list[i:i+4] for i in range(0, len(b_list), 4)]
count2=0
#S盒
for temp in small_lists:
    t1=temp+b_small[count2]
    t2=temp+b_small[count2+1]
    t3=b_small[count2]+temp
    t4=b_small[count2+1]+temp
    problem.linear_constraints.add(lin_expr=[[t1, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t2, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t3, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t4, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    temp.pop()
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    count2+=2
#print(count1)
#异或
t1=[]
for i in range(321,385):
    t1.append('x'+str(i))
t1_lists = [t1[i:i+4] for i in range(0, len(t1), 4)]
t2=[]
for i in range(385,417):
    t2.append('x'+str(i))
t2_lists = [t2[i:i+4] for i in range(0, len(t2), 4)]
s1=[]
s2=[]
for i in range(len(t1_lists)):
    if i%2==0:
        s1.append(t1_lists[i])
    else:
        s2.append(t1_lists[i])
#print(s1)
temp=s2.pop(0)
s2.append(temp)
#print(s2)
#count3=1
for i in range(0,len(s1)):
    for j in range(0,4):
        temp=[]
        temp.append(s1[i][j])
        temp.append(s2[i][j])
        temp.append(t2_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1

#移位
tt=[0]*8
tt[0]=t2_lists[7]
tt[1]=t2_lists[4]
tt[2]=t2_lists[1]
tt[3]=t2_lists[6]
tt[4]=t2_lists[3]
tt[5]=t2_lists[0]
tt[6]=t2_lists[5]
tt[7]=t2_lists[2]
#print(tt)

t3=[]
for i in range(161,193):
    t3.append('x'+str(i))
t3_lists = [t3[i:i+4] for i in range(0, len(t3), 4)]

t4=[]
for i in range(417,449):
    t4.append('x'+str(i))
t4_lists = [t4[i:i+4] for i in range(0, len(t4), 4)]

for i in range(0,len(tt)):
    for j in range(0,4):
        temp=[]
        temp.append(tt[i][j])
        temp.append(t3_lists[i][j])
        temp.append(t4_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1
#第三轮结束


all_list=[]
for i in range(417,449):
    all_list.append('x'+str(i))
small_lists = [all_list[i:i+4] for i in range(0, len(all_list), 4)]
b_list=[]
for i in range(449,513):
    b_list.append('x'+str(i))
b_small=[b_list[i:i+4] for i in range(0, len(b_list), 4)]
count2=0
#print(b_small)
#S盒
for temp in small_lists:
    t1=temp+b_small[count2]
    t2=temp+b_small[count2+1]
    t3=b_small[count2]+temp
    t4=b_small[count2+1]+temp
    problem.linear_constraints.add(lin_expr=[[t1, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t2, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t3, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[t4, [4.0,4.0,4.0,4.0, -1.0,-1.0,-1.0,-1.0]]], senses=['G'], rhs=[0])
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    temp.pop()
    temp.append('a'+str(count1))
    problem.linear_constraints.add(lin_expr=[[temp, [1.0,1.0,1.0,1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    problem.linear_constraints.add(lin_expr=[[[temp[4],temp[3]], [1.0, -1.0]]], senses=['G'], rhs=[0])
    count1+=1
    count2+=2
#print(count1)
#异或
t1=[]
for i in range(449,513):
    t1.append('x'+str(i))
t1_lists = [t1[i:i+4] for i in range(0, len(t1), 4)]
t2=[]
for i in range(513,545):
    t2.append('x'+str(i))
t2_lists = [t2[i:i+4] for i in range(0, len(t2), 4)]
s1=[]
s2=[]
for i in range(len(t1_lists)):
    if i%2==0:
        s1.append(t1_lists[i])
    else:
        s2.append(t1_lists[i])
#print(s1)
temp=s2.pop(0)
s2.append(temp)
#print(s2)
#count3=1
for i in range(0,len(s1)):
    for j in range(0,4):
        temp=[]
        temp.append(s1[i][j])
        temp.append(s2[i][j])
        temp.append(t2_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1

#移位
tt=[0]*8
tt[0]=t2_lists[7]
tt[1]=t2_lists[4]
tt[2]=t2_lists[1]
tt[3]=t2_lists[6]
tt[4]=t2_lists[3]
tt[5]=t2_lists[0]
tt[6]=t2_lists[5]
tt[7]=t2_lists[2]
#print(tt)

t3=[]
for i in range(289,321):
    t3.append('x'+str(i))
t3_lists = [t3[i:i+4] for i in range(0, len(t3), 4)]

t4=[]
for i in range(545,577):
    t4.append('x'+str(i))
t4_lists = [t4[i:i+4] for i in range(0, len(t4), 4)]

for i in range(0,len(tt)):
    for j in range(0,4):
        temp=[]
        temp.append(tt[i][j])
        temp.append(t3_lists[i][j])
        temp.append(t4_lists[i][j])
        temp.append('d'+str(count3))
        problem.linear_constraints.add(lin_expr=[[temp, [1.0, 1.0,1.0,-2.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[0]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[1]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[3],temp[2]], [1.0, -1.0]]], senses=['G'], rhs=[0])
        problem.linear_constraints.add(lin_expr=[[[temp[0],temp[1],temp[2]], [1.0, 1.0,1.0]]], senses=['L'], rhs=[2])
        count3+=1
#第四轮结束
total=[]
for i in range(1,33):
    total.append('x'+str(i))
#print(total)
a=[1.0]*len(total)
problem.linear_constraints.add(lin_expr=[[total, a]], senses=['G'], rhs=[1])

problem.solve()

print("Solution status: ", problem.solution.get_status())
print("Objective value: ", problem.solution.get_objective_value())
print("Solution:")
solution=problem.solution.get_values()

print("x ",solution[:x_number])
print("a ",solution[x_number:x_number+a_number])
print("d ",solution[x_number+a_number:x_number+a_number+d_number])


