
from numpy import *

data = load('traj.npz')
lst = data.files
matriz = zeros((8,8))
for item in unique(data['traj'],axis=0):
    matriz[int(item[0]),int(item[2])] = int(item[1])
for ii in matriz:
    pe = ''
    for jj in ii:
        pe +=str(int(jj))+','
    print(pe[:-1])

for item in lst:
    print(item)
    for x in data[item]:
        if x[0] == 0
        print(x)