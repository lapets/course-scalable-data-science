from random import random
import sys
import os
import multiprocessing as mp
from timeit import default_timer as timer
from functools import reduce
from functools import partial
from parts import parts

def trial(instance):
    (x, y) = (2*random()-1, 2*random()-1)
    return {
        "in":1 if (x**2 + y**2) <= 1 else 0, 
        "count":1
      }

def combine(t1, t2):
    return {"in":t1["in"]+t2["in"], "count":t1["count"]+t2["count"]}

#result = reduce(combine, map(trial, range(1000000)))
#print(result, 4*result["in"]/float(result["count"]))

def map_mp(pool, op, xs):
    return pool.map(partial(map, op), parts(xs, pool._processes))

def reduce_mp(pool, op, xs_per_part):
    return reduce(op, pool.map(partial(reduce, op), xs_per_part))

if __name__ == '__main__':
    ps = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    pool = mp.Pool(processes=ps,) #mp.cpu_count()
    print("Starting.")
    start = timer()
    ps = map_mp(pool, trial, range(1000000))
    r = reduce_mp(pool, combine, ps)
    print("Finished in " + str(timer() - start) + " seconds.")
    print(4*r['in']/float(r['count']))

## eof