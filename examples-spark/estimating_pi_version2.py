from pyspark import SparkContext
from pyspark.sql.functions import rand


# sc = SparkContext("local", "Pi apprximation version 2")
# iteration=1000000
# partition=4
# data = range(0,iteration)
# distIn = sc.parallelize(data,partition)
# result=distIn.map(lambda n:(1 if n%2==0 else -1)/float(2*n+1)).reduce(lambda a,b: a+b)

def trial(instance):
    (x, y) = (2*random()-1, 2*random()-1)
    return {
        "in":1 if (x**2 + y**2) <= 1 else 0, 
        "count":1
      }

def combine(t1, t2):
    return {"in":t1["in"]+t2["in"], "count":t1["count"]+t2["count"]}


var result = reduce(combine, map(trial, range(1000000)))

print "Pi is %f" % (4 * result["in"] / float(result["count"]))
