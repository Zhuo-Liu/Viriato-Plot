import numpy as np
from matplotlib import pyplot as plt

def read_invariants(f_path):
    f = open(f_path)
    names = f.readline().split()


f = open('./gm10_invariants.dat')
f2 = open('./gm10_2_invariants.dat')

names = f.readline().split()
L = len(names)

times = []
eta = []
nu = []
gm = []
gmk = []

for i in range(678):
    line = f.readline().split()
    line_num = [float(entry) for entry in line]
    time = line_num[0]
    hyper_eta, hyper_nu, hyper_gm, hyper_gmk = line_num[11],line_num[12],line_num[13],line_num[14]
    times.append(time)
    eta.append(hyper_eta)
    nu.append(hyper_nu)
    gm.append(hyper_gm)
    gmk.append(hyper_gmk)

f.close()

for i in range(672):
    line = f2.readline().split()
    if i > 35:
        line_num = [float(entry) for entry in line]
        time = line_num[0]
        hyper_eta, hyper_nu, hyper_gm, hyper_gmk = line_num[11],line_num[12],line_num[13],line_num[14]
        times.append(time)
        eta.append(hyper_eta)
        nu.append(hyper_nu)
        gm.append(hyper_gm)
        gmk.append(hyper_gmk)

f2.close()
#plt.figsize((12,8))
gm = np.array(gm)
gmk = np.array(gmk)

gd = gm + gmk
plt.plot(times,eta,label='eta')
plt.plot(times,nu,label='nu')
plt.plot(times,gd,label='gm')

plt.legend()
plt.show()



# print(names)