from pyspark import SparkContext
import random

def trial(instance):
    (x, y) = (2*random.random()-1, 2*random.random()-1)
    return {
         "in":1 if (x**2 + y**2) <= 1 else 0, 
         "count":1
    }

def combine(t1, t2):
    return {"in":t1["in"]+t2["in"], "count":t1["count"]+t2["count"]}


result = reduce(combine, map(trial, range(1000000)))

print "Pi is %f" % (4 * result["in"] / float(result["count"]))