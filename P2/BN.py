# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

import numpy as np
import itertools
np.set_printoptions(precision=4, suppress=True)


class Node():
    def __init__(self, prob, parents = []):
        self.parents = parents
        self.prob = prob

    
    def computeProb(self, evid):
        if self.parents == []:
            return [1-self.prob[0],self.prob[0]]
        val = self.prob
        for i in range(0,len(self.parents)):
            val = val[evid[self.parents[i]]]
        return [1-val,val]


    
class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob

    def computePostProb(self, evid):
        evid = list(evid)
        evTested = evid.index(-1)
        evid[evTested] = 1
        negative_evs = list(evid)
        negative_evs[evTested] = 0
        evsTorF = [i for i, e in enumerate(evid) if e == []] #indexes in array evid of unknown variables
        combinations = [item for item in itertools.product([0,1], repeat=len(evsTorF))] #possible combinations between these variables
        positive = negative = 0
        for c in combinations:
            for i in range(len(c)):
                evid[evsTorF[i]] = c[i]
                negative_evs[evsTorF[i]] = c[i]
            positive += self.computeJointProb(evid)
            negative += self.computeJointProb(negative_evs)
        return positive / (positive + negative)

    def computeJointProb(self, evid):
        """
        p = [1,1]
        for i in range(0,len(self.gra)):
            for j in range(0,len(self.gra)):
                p[i] *= self.prob[j].computeProb(evid)[i]
        return p
        """
        p = 1
        for i in range(len(evid)):
            p *= self.prob[i].computeProb(evid)[evid[i]]
        return p
        


p3 = Node( np.array([[.001,.29],[.94,.95]]), [0,1] )
ev = (0,0,1,1,1)
print(p3.computeProb(ev))

ev = (1,1,1,1,1)
print(p3.computeProb(ev))



gra = [[],[],[0,1],[2],[2]]
p1 = Node( np.array([.001]), gra[0] ) # burglary
#print( "%.4e" % p1.computeProb(ev)[0])
p2 = Node( np.array([.002]), gra[1] ) # earthquake
p3 = Node( np.array([[.001,.29],[.94,.95]]), gra[2] ) # alarm
#print( "%.4e" % p3.computeProb(ev)[0])
p4 = Node( np.array([.05,.9]), gra[3] ) # johncalls
p5 = Node( np.array([.01,.7]), gra[4] ) # marycalls
prob = [p1,p2,p3,p4,p5]
gra = [[],[],[0,1],[2],[2]]
bn = BN(gra, prob)

#print("joint ", bn.computeJointProb((1,1,1,1,0)))

#print("----\n")
#print(bn.computePostProb( (-1,[],[],1,1) ))


