from vbench.benchmark import Benchmark

getset_fancy_setup = """
from scipy.sparse import lil_matrix
from numpy import where, zeros, prod, vstack, ones
from time import time

n, m = 1000, 2000
M = vstack((zeros((n, m)), ones((25, m)))) # this changes time for lil very sufficiently
I, J = where(M)

M = lil_matrix(M)

def doit_lil():
    M[I, J]
"""

lil_getset_fancy = Benchmark("doit_lil()", setup=getset_fancy_setup, name="lil_getset_fancy")
