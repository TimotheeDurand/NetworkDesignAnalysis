

import networkx as nx
import matplotlib.pyplot as plt
import random

def greedy(k,p,chi_size,G,nodes,edges):


    ###########################
    #sample/scenarios X in Chi#
    ###########################
    
    chi = set()
    
    while len(chi) < chi_size:
        liveArcs = []
        for edge in edges:
            edgeIsActive = random.random() < p
            if edgeIsActive == True:
                liveArcs.append(edge)
              
        if len(liveArcs) == 0:
            chi.add(frozenset())
        else:
            X = frozenset(liveArcs)
            chi.add(X)
    
    
    ##################
    #Greedy Algorithm#
    ##################
    
    GX = nx.DiGraph()
    GX.add_nodes_from(nodes)
  
    A = set()
    
    while len(A) < k:
        
        
        sigmas = {}
        mySum = []
        for X in chi:
            GX.add_edges_from(X)
            
            R = set()
            for i in A:
                R_iX = nx.algorithms.dag.descendants(GX,i)
                R.update(R_iX)
                
            for v in nodes:
                if v not in A:
                    
                    R_vX = nx.algorithms.dag.descendants(GX,v)
                    R.update(R_vX)
                    
                    
                    sigma_X = len(R)
                    mySum.append(sigma_X)
    
            
                sig_Auv =(1/len(chi)) * sum(mySum)
                sigmas[v] = sig_Auv
            
            GX.remove_edges_from(X)
                    
                        
        max_sigma = max(sigmas, key = lambda x: sigmas.get(x))
        A.update({max_sigma})
        
        

    
    #draw graph#
    '''
    plt.subplot(121)
    nx.draw(G,with_labels = True)
    
    plt.subplot(122)
    nx.draw(GX,with_labels = True)
    '''
            
    return A