# Scalable Data Science

These notes go over a small number of related topics in the area of scalable, distributed computing as it applies to scenarios in data science.

## Background and Context

Within computer science and related fields there exist a large number of mathematical models, paradigms, and tools for analyzing, defining, and implementing computations that take advantage of distributed computing resources (such as [multicore processing](https://en.wikipedia.org/wiki/Multi-core_processor), high-performance [computing clusters](https://en.wikipedia.org/wiki/Computer_cluster), [clouds](https://en.wikipedia.org/wiki/Cloud_computing), and so on). 

In particular, a variety of taxonomies exist for categorizing both computational resources (such as [Flynn's taxonomy](https://en.wikipedia.org/wiki/Flynn%27s_taxonomy)) and for distinguishing techniques (e.g., [data parallelism](https://en.wikipedia.org/wiki/Data_parallelism) vs. [task parallelism](https://en.wikipedia.org/wiki/Task_parallelism). Furthermore, there exist many ways to classify problems in terms of their amenability to different distributed computing or parallelization techniques. With the advent of contemporary cloud computing environments these distinctions are less rigid; setting up an infrastructure to match a problem is becoming quicker and easier.

Dealing with only a small region of this broad landscape, these notes discuss only a particular family of paradigms and tools for solving *algebraically decomposable problems* (in which communication costs between concurrent operations are fairly limited and primarily one-way) using homogenous distributed storage and computing resources (typically available in a contemporary cloud computing environment such as Amazon Web Services). Whether these are useful in a given situation depends on the particular properties of the problem and the types of distributed computing resources available. Some ways to determine the suitability of these techniques or the scalable solvability of a given problem are discussed and illustrated through examples.

## Definitions

We present a number of definitions to establish a well-defined vocabulary that will be used throughout these notes. These definitions may have other variants or scopes in other materials outside of these notes.

A *set* or *dimension* is some mathematical object. Examples of sets include the natural numbers (i.e., `{0, 1, 2, 3, ...}`), the set of all strings, and so on. 

A *tuple* is an ordered list of elements drawn from sets. Each entry in the list is called a *component*. For example, `(123, "abc")` is a tuple with the first component drawn from the set of natural numbers and the second component drawm from the set of string. It is possible to have sets of tuples.

A *data record* or *dictionary* is a mapping from a set of *attributes* (typically strings) to *values* drawn from some set. One example is `{"name": "Alice", "age": 25}`. In the contemporary web ecosystem, a common format for representing records is [JSON](https://en.wikipedia.org/wiki/JSON#Example) (e.g., MongoDB uses such a format natively). In Python, these can be represented faithfully using the native [dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) data structure.

A *data set* is an unordered collection of records. A data set could be viewed/treated as a table within a data base (e.g., see [attribute-value system](https://en.wikipedia.org/wiki/Attribute-value_system)).

A *key-value store* is a data set in which each record is associated with an identifying *key* that is unique to that record.

## Algebraic Properties and Scalable Computation

The particular family of scalable and distributed computation paradigms on which these notes focus relies heavily on the algebraic properties of computations over data. If we treat individual data records as elements in a set and computations as operations over those elements, we can talk about their algebraic properties.

You are already familiar with several important algebraic properties: associativity and commutativity. These properties apply to operations such as addition, multiplication, union, intersection, maximum/minimum, and others:
* *a* + *b* = *b* + *a*
* *x* &middot; (*y* &middot; *z*) = (*x* &middot; *y*) &middot; *z*
* **max**(*x*, *y*) = **max**(*y*, *x*)
* {1,2,3} &cup; {4,5} = {4,5} &cup; {1,2,3}

Another useful algebraic property is *idempotence*. An operation is idempotent if applying it once leads to the same result as applying it any number of times after that. Example of idempotent operations include union and maximum:
* **max**(**max**(**max**(*x*, *y*), *y*), *y*) = **max**(*x*, *y*)
* {1,2} &cup; {3,4} &cup; {3,4} &cup; {3,4} &cup; {3,4} = {1,2} &cup; {3,4}

### MapReduce Paradigm

A well-known example of a paradigm that takes advantage of these properties is MapReduce. To understand this paradigm, it is first easier to consider how you might compute common operations on a list of numbers.

#### Reduce Operations

For example, if we have a collection of numbers we can compute the sum or the maximum across all the numbers by repeatedly grabbing numbers from the collection and combining them using a binary operation:
* **&Sigma;** {1, 2, 3, 4, 5} = (1 + 2) + (3 + (4 + 5))
* **maximum** {1, 2, 3, 4, 5} = **max**(**max**(2, 5), **max**(**max**(1, 4), 5))

Effectively, we have *decomposed* the overall operation into a series of applications of a binary operation. Notice that because the binary operations are associative and commutative, the order in which we do this does not matter.

In general, we can call this process *reduction*, and define a generic *reduce* function that takes any binary operation and applies it to a list (in any order it chooses). Exactly such a function (also called `reduce`) exists in Python:
```python
>>> from functools import reduce
>>> reduce(max, [1,2,3,4,5])
5
>>> from operator import add
>>> add(1,2)
3
>>> reduce(add, [1,2,3,4,5])
15
```
We can easily implement this Python function ourselves:
```python
def reduce(op, xs):
    r = xs[0] # Our running aggregate result.
    for x in xs[1:]: # Start at second element at index 1.
        r = op(r, x)
    return r
```

#### Applying Reduce to Data Sets

If we want to apply the reduce function to an actual data set of records, we might need to define a binary operation that works on records. For instance, suppose we have a data set representing individuals:
```python
D = [{"name":"Alice", "age":24}, 
     {"name":"Bob", "age":20}, 
     {"name":"Carol", "age":31}]
```
We need to define a custom addition operation that can operate on records.
```python
def max_age(r1, r2):
    return {"age":max(r1["age"], r2["age"])}
```
We can then use the `reduce` function as before:
```python
>>> reduce(max_age, D)
{"age": 31}
```

#### Map Operations

The approach above works well in many situations but can present difficulties. Suppose we want to use a reduce operation to compute the average age. Unfortunately, the binary version of the average operator is not associative (note that the correct average age is 25):
* **avg**(**avg**(24, 20), 31) = 26.5 &ne; 24.75 = **avg**(24, **avg**(20, 31))

However, we can address this by using a *weighted* average. We would first prepare the data by augmenting it with its weight. We would then extend the binary operator to incorporate the weight.
```python
def age_wgtd(r):
    return {"age":r["age"], "wgt":1}

def avg_age_wgtd(r1, r2):
    return {"age":r1["age"] + r2["age"], "wgt":r1["wgt"] + r2["wgt"]}
```
Notice that we also took the opportunity above to drop the `"name"` attribute, which we do not need in the rest of the computation (nor does it make sense to have an individual name for an aggregate total within the context of the example). We then *map* the `age_wgtd` function across the data set records before applying our reduce operation.
```python
>>> map(age_wgtd, D)
[{"age":24, "wgt":1}, {"age":20, "wgt":1}, {"age":31, "wgt":1}]
>>> reduce(avg_age_wgtd, D)
[{"age":75, "wgt":3}]
```
The above gives us exactly one record from which we can compute the correct average of 75/3 = 25.

In most frameworks, the operation that is applied using the map function is more general: it could return no results or many results (thus providing a way to *generate* data that can later be reduced) and might involve a lengthy computation of its own.

In Python, there is a more concise and mathematically familiar way to define this behavior natively using [comprehensions](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions):
```python
>>> [age_wgtd(r) for r in D]
[{"age":24, "wgt":1}, {"age":20, "wgt":1}, {"age":31, "wgt":1}]
```
Note also that, as with `reduce`, we can implement our own generic `map` function, as well.
```python
def map(op, xs):
    ys = [] # Our running aggregate result.
    for x in xs:
        ys += [op(x)]
    return ys
```

### Example: Estimating &pi;

Suppose we want to estimate &pi;. We know that &pi; is the area of the unit circle (&pi; &middot; 1<sup>2</sup> = &pi;), so one way to approach this is to generate many random points (*x*, *y*) between (-1, -1) and (1, 1) (i.e., a square of area 2 &middot; 2 = 4 centered on the origin) and to count how many are at most a distance of 1 from the origin (i.e., *x*<sup>2</sup> + *y*<sup>2</sup> &le; 1). In general, we should expect about *area(circle)*/*area(square)* = &pi;/4 of the points to be in the circle, so we would only need to multiply the ratio we obtain by 4 to estimate &pi;.

We can first define the operations that the map and reduce steps will perform.
```python
from random import random

def trial(instance):
    (x, y) = (2*random()-1, 2*random()-1)
    return {
        "in":1 if (x**2 + y**2) <= 1 else 0, 
        "count":1
      }

def combine(t1, t2):
    return {"in":t1["in"]+t2["in"], "count":t1["count"]+t2["count"]}
```
Then, our overall result can be obtained using `map` and `reduce`:
```python
>>> result = reduce(combine, map(trial, range(1000000)))
>>> result
{'count': 1000000, 'in': 785272}
>>> 4 * result["in"] / float(result["count"])
3.141088
```

### Example: Computing Word Frequencies

## Building Indices

A computation applied to a large data set to solve some problem will often need to access various parts of that data set throughout the computation. This is potentially where a large portion of the cost of the computation lies. One way to address this is by building an *index* that allows easier retrieval of records from the data set using some relevant information.

Fortunately, the problem of building an index can often be decomposed into the application of an associative and commutative (and sometimes even idempotent) operator. 

## Appendix

The examples in these notes rely on Python 3. You should [download and install Python 3](https://www.python.org/) if you want to replicate or interactively explore the examples.