# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

import numpy as np
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


               
        return 0
        
        
    def computeJointProb(self, evid):
        """
        p = [1,1]
        for i in range(0,len(self.gra)):
            for j in range(0,len(self.gra)):
                p[i] *= self.prob[j].computeProb(evid)[i]
        return p
        """
        p = 1
        for i in range(0,len(self.gra)):
            p *= self.prob[i].computeProb(evid)[1]
        return p
        

"""
p3 = Node( np.array([[.001,.29],[.94,.95]]), [0,1] )
ev = (0,0,1,1,1)
print(p3.computeProb(ev))

ev = (1,1,1,1,1)
print(p3.computeProb(ev))

"""
