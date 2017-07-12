from random import random
import sys
import os
import multiprocessing as mp
from timeit import default_timer as timer
from functools import reduce
from functools import partial
from parts import parts
import numpy as np

def map_mp(pool, op, xs):
    return pool.map(partial(map, op), parts(xs, pool._processes))

def reduce_mp(pool, op, xs_per_part):
    return reduce(op, pool.map(partial(reduce, op), xs_per_part))

def closest(ms, p):
    return list(sorted([(np.linalg.norm(np.subtract(m,p)), m) for m in ms]))[0][1]

def assign(means, point):
    return {closest(means, point): (point, 1, point)}

zero = ((0,0), 0, 0)

def add(r1, r2):
    (vec1, wgt1, m1) = r1
    (vec2, wgt2, m2) = r2
    (vec, wgt) = (np.add(vec1, vec2), wgt1 + wgt2)
    return (vec, wgt, tuple(np.multiply(vec, 1/wgt))) 

def combine(mp1, mp2):
    return {m:add(mp1.get(m,zero), mp2.get(m,zero)) for m in mp1.keys() | mp2.keys()}

if __name__ == '__main__':
    ps = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    pool = mp.Pool(processes=ps,) #mp.cpu_count()

    P = [(1,0),(4,5),(7,3),(5,2),(1,3),(27,34),(37,29),(25,27)]*10000
    M = [(13,13), (14,14)]

    print("Starting.")
    start = timer()
    M_OLD = None
    while M_OLD != M:
        M_OLD = M
        ps = map_mp(pool, partial(assign, M), P)
        M = reduce_mp(pool, combine, ps)
        M = [m for (m_old, (t, c, m)) in M.items()]
    print("Finished in " + str(timer() - start) + " seconds.")
    print(M)

## eof