#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 20:47:43 2019

@author: gracie
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
import time


def out_degree(G,k):
    
    mydict = dict(G.out_degree(list(G)))
    A = set()
    
    while len(A) < k:
    
        highest_degree = max(mydict, key = lambda x: mydict.get(x))
        mydict.pop(highest_degree)
        
        A.add(highest_degree)
        
    return A

def centrality(G,k):
    
    centrality_dict = nx.algorithms.centrality.closeness_centrality(G)
    
    A = set()
    while len(A) < k:
        
        highest_centrality = max(centrality_dict, key = lambda x: centrality_dict.get(x))
        centrality_dict.pop(highest_centrality)
        
        A.add(highest_centrality)
    
    return A