from vbench.benchmark import Benchmark

getset_fancy_setup = """
from scipy import sparse
from numpy import where, zeros, prod, vstack, ones
from time import time

n, m = 1000, 2000
M = vstack((zeros((n, m)), ones((25, m))))
I, J = where(M)
v = np.ones_like(I)

M = sparse.{format}_matrix(M)

def do_get():
    M[I, J]

def do_set():
    M[I, J] = v
"""

for format in ['csr', 'csc']:
    for action in ['get', 'set']:
        fmt = lambda x: x.format(action=action, format=format)
        bench = Benchmark(fmt("do_{action}()"),
                          setup=fmt(getset_fancy_setup),
                          name=fmt("{format}_{action}_fancy"))
        exec(fmt('vb_{format}_{action}_fancy = bench'))
        del bench
