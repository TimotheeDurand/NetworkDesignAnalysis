

import networkx as nx
import matplotlib.pyplot as plt
import random
from reachable import reachable_nodes

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
            
            print(A)
            
            GX.add_edges_from(X)
            
            R = set()
            R_forall_nodes = []
            
            
            for i in nodes:
                R_iX = reachable_nodes(GX,i)
                R_forall_nodes.append(R_iX)
            
            for i in A:
                R.update(R_forall_nodes[i-1])
                
            for v in nodes:
                if v not in A:
                    
                    R.update(R_forall_nodes[v-1])
                    
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