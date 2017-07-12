import json
import geojson
import shapely.geometry
import rtree
from tqdm import tqdm

import sys
import multiprocessing as mp
from timeit import default_timer as timer
from functools import reduce, partial
from parts import parts

def map_mp(pool, op, xs):
    return pool.map(partial(map, op), parts(xs, pool._processes))

def reduce_mp(pool, op, xs_per_part):
    return reduce(op, pool.map(partial(reduce, op), xs_per_part))

def assign(rt, f):
    student_to_stop = {}
    (lon, lat) = f["geometry"]["coordinates"][0]
    index = next(rt.nearest((lon, lat, lon, lat), 1))
    student_to_stop[(lon, lat)] = index
    return student_to_stop

if __name__ == '__main__':
    ps = 1 if len(sys.argv) == 1 else int(sys.argv[1])
    rt = rtree.index.Index()
    points = []
    grid = geojson.load(open("streetgrid.geojson"))
    for f in grid["features"]:
        if f["type"] == "Point":
            (lon, lat) = f["coordinates"]
            index = len(points)
            points.append((lon, lat))
            rt.insert(index, [lon, lat, lon, lat])
    students = geojson.load(open("students.geojson"))["features"]
    pool = mp.Pool(processes=ps,) #mp.cpu_count()
    print("Starting.")
    start = timer()
    student_to_stop_parts = map_mp(pool, partial(assign, rt), list(students))
    print("Finished in " + str(timer() - start) + " seconds.")

##eof
