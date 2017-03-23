import numpy as np
import scipy as sp
import sys

def BellmanFord(ist,isp,wei):
    #----------------------------------
    #  ist:    index of starting node
    #  isp:    index of stopping node
    #  wei:    adjacency matrix (V x V)
    #
    #  shpath: shortest path
    #----------------------------------

    V = wei.shape[1]

    # step 1: initialization
    Inf    = sys.maxint
    d      = np.ones((V),float)*np.inf
    p      = np.zeros((V),int)*Inf
    d[ist] = 0

    # step 2: iterative relaxation
    for i in range(0,V-1):
        for u in range(0,V):
            for v in range(0,V):
                w = wei[u,v]
                if (w != 0):
                    if (d[u]+w < d[v]):
                        d[v] = d[u] + w
                        p[v] = u

    # step 3: check for negative-weight cycles
    for u in range(0,V):
        for v in range(0,V):
            w = wei[u,v]
            if (w != 0):
                if (d[u]+w < d[v]):
                    print('graph contains a negative-weight cycle')

    # step 4: determine the shortest path
    shpath = [isp]
    while p[isp] != ist:
        shpath.append(p[isp])
        isp = p[isp]
    shpath.append(ist)

    return shpath[::-1]


if __name__ == '__main__':

    # indices of starting and stopping vertices
    ist = 4
    isp = 3

    # randomly generated adjacency matrix
    #N   = 10
    #ma  = np.around(np.random.uniform(0,1.2,(N,N)))
    #wei = ma*np.random.uniform(0,30,(N,N))
    #wei = np.tril(wei,-1) + np.triu(wei,1)

    # adjacency matrix
    wei = np.array([[ 0, 20,  0, 80, 0,  0, 90,  0],
                    [ 0,  0,  0,  0, 0, 10,  0,  0],
                    [ 0,  0,  0, 10, 0, 50,  0, 20],
                    [ 0,  0, 10,  0, 0,  0, 20,  0],
                    [ 0, 50,  0,  0, 0,  0, 30,  0],
                    [ 0,  0, 10, 40, 0,  0,  0,  0],
                    [20,  0,  0,  0, 0,  0,  0,  0],
                    [ 0,  0,  0,  0, 0,  0,  0,  0]])

    # minimal distance path
    shpath = BellmanFord(ist,isp,wei)
    print ist,' -> ',isp,' is ',shpath
