import numpy as np
import scipy as sp
import math as ma
import sys
import time

def Dijkstra(ist,isp,wei):
    # Dijkstra algorithm for shortest path in a graph
    #    ist: index of starting node
    #    isp: index of stopping node
    #    wei: weight matrix

    # exception handling (start = stop)
    if (ist == isp):
        shpath = [ist]
        return shpath

    # initialization
    N         =  len(wei)
    Inf       =  sys.maxint
    UnVisited =  np.ones(N,int)
    cost      =  np.ones(N)*1.e6
    par       = -np.ones(N,int)*Inf

    # set the source point and get its (unvisited) neighbors
    jj            = ist
    cost[jj]      = 0
    UnVisited[jj] = 0
    tmp           = UnVisited*wei[jj,:]
    ineigh        = np.array(tmp.nonzero()).flatten()
    L             = np.array(UnVisited.nonzero()).flatten().size

    
    # start Dijkstra algorithm
    while (L != 0):
        # step 1: update cost of unvisited neighbors,
        #         compare and (maybe) update
        for k in ineigh:
            newcost = cost[jj] + wei[jj,k]
            if ( newcost < cost[k] ):
                cost[k] = newcost
                par[k]  = jj

        # step 2: determine minimum-cost point among UnVisited
        #         vertices and make this point the new point
        icnsdr     = np.array(UnVisited.nonzero()).flatten()
        cmin,icmin = cost[icnsdr].min(0),cost[icnsdr].argmin(0)
        jj         = icnsdr[icmin]

        # step 3: update "visited"-status and determine neighbors of new point
        UnVisited[jj] = 0
        tmp           = UnVisited*wei[jj,:]
        ineigh        = np.array(tmp.nonzero()).flatten()
        L             = np.array(UnVisited.nonzero()).flatten().size
    # determine the shortest path
    shpath = [isp]
    while par[isp] != ist:
        shpath.append(par[isp])
        isp = par[isp]
    shpath.append(ist)

    return shpath[::-1]

def calcWei(RX,RY,RA,RB,RV):
    # calculate the weight matrix between the points

    n    = len(RX)
    wei = np.zeros((n,n),dtype=float)
    m    = len(RA)
    for i in range(m):
        xa = RX[RA[i]-1]
        ya = RY[RA[i]-1]
        xb = RX[RB[i]-1]
        yb = RY[RB[i]-1]
        dd = ma.sqrt((xb-xa)**2 + (yb-ya)**2)
        tt = dd/RV[i]
        wei[RA[i]-1,RB[i]-1] = tt
    return wei

if __name__ == '__main__':

    import numpy as np
    import scipy as sp
    import csv

    # EXAMPLE 1
    # starting and stopping node
    #ist = 4
    #isp = 3
    # adjacency matrix
    #wei = np.array([[ 0, 20,  0, 80, 0,  0, 90,  0],
    #                [ 0,  0,  0,  0, 0, 10,  0,  0],
    #                [ 0,  0,  0, 10, 0, 50,  0, 20],
    #                [ 0,  0, 10,  0, 0,  0, 20,  0],
    #                [ 0, 50,  0,  0, 0,  0, 30,  0],
    #                [ 0,  0, 10, 40, 0,  0,  0,  0],
    #                [20,  0,  0,  0, 0,  0,  0,  0],
    #                [ 0,  0,  0,  0, 0,  0,  0,  0]])
    #shpath = Dijkst(ist,isp,wei)
    #print ist,' -> ',isp,' is ',shpath

    # EXAMPLE 2 (path through Rome)
    RomeX = np.empty(0,dtype=float)
    RomeY = np.empty(0,dtype=float)
    with open('RomeVertices','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeX = np.concatenate((RomeX,[float(row[1])]))
            RomeY = np.concatenate((RomeY,[float(row[2])]))
    file.close()

    RomeA = np.empty(0,dtype=int)
    RomeB = np.empty(0,dtype=int)
    RomeV = np.empty(0,dtype=float)
    with open('RomeEdges','r') as file:
        AAA = csv.reader(file)
        for row in AAA:
            RomeA = np.concatenate((RomeA,[int(row[0])]))
            RomeB = np.concatenate((RomeB,[int(row[1])]))
            RomeV = np.concatenate((RomeV,[float(row[2])]))
    file.close()

    wei = calcWei(RomeX,RomeY,RomeA,RomeB,RomeV)

    ist = 12 # St. Peter's Square
    isp = 51 # Coliseum

    # use the Bellman-Ford algorithm
    t0 = time.time()
    shpath = BellmanFord(12,51,wei)
    t1 = time.time()
    print 'Bellman-Ford: ',ist+1,' -> ',isp+1,' is ',np.array(shpath)+1,t1-t0

    # use the Dijkstra algorithm
    t0 = time.time()
    shpath = Dijkst(12,51,wei)
    t1 = time.time()
    print 'Dijkstra:     ',ist+1,' -> ',isp+1,' is ',np.array(shpath)+1,t1-t0
