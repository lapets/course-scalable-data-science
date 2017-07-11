from random import random
import sys
import os
import multiprocessing as mp
from timeit import default_timer as timer
from functools import reduce
from functools import partial
from parts import parts

def map_mp(pool, op, xs):
    return pool.map(partial(map, op), parts(xs, pool._processes))

def reduce_mp(pool, op, xs_per_part):
    return reduce(op, pool.map(partial(reduce, op), xs_per_part))

import json

def index(article):
    return {word:{article['id']} for word in set(article['text'].split(" "))}

def combine(i, j):
    return {k:(i.get(k,set()) | j.get(k,set())) for k in i.keys() | j.keys()}

if __name__ == '__main__':
    ps = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    pool = mp.Pool(processes=ps,) #mp.cpu_count()
    articles = json.load(open('nyt.json','r'))
    print("Starting.")
    start = timer()
    ps = map_mp(pool, index, articles)
    r = reduce_mp(pool, combine, ps)
    print("Finished in " + str(timer() - start) + " seconds.")
    open('index.json', 'w').write(json.dumps({w:list(r[w]) for w in r}, indent=2))

## eof