#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 18:49:18 2019

@author: gracie
"""
import networkx as nx

def reachable_nodes(GX,v):
    R_vX = set()
    for i in list(GX):
        if nx.has_path(GX,v,i):
            R_vX.add(i)
            
    return R_vX
