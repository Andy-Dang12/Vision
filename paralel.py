# https://viblo.asia/p/giai-phap-tang-performance-python-code-parallel-programming-QpmlewnNKrd
# https://docs.python.org/3/library/multiprocessing.html
import math
import os
from multiprocessing import Pool, Process
from time import time
from colorama import Fore


def cacu_size(x):
    return math.sqrt(x**3)


x = 100000000
s = time()
a = []
for i in range(x):
    a.append(cacu_size(i))
ss = time()
print(ss-s)
print(a[-2:])
print(Fore.RED,"start paralel")

t = time()
with Pool(processes=os.cpu_count()) as pool:
    aaa = pool.map(cacu_size, range(x))
tt = time()

print(tt-t)
print(aaa[-2:])

