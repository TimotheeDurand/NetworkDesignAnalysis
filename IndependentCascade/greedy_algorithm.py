

import networkx as nx
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
            myrand = random.random()
            edgeIsActive = myrand < p
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
    
    
    reachable_nodes_inGX = []
    
    for X in chi:
        GX = nx.DiGraph()
        GX.add_nodes_from(nodes)
        GX.add_edges_from(X)

        
        R_GX = []
        for i in nodes:
            R_iX = reachable_nodes(GX,i)
            R_GX.append(R_iX)


        reachable_nodes_inGX.append(R_GX)

        

    A = set()
    
    
    while len(A) < k:
        
        
        sigmas = {}
        
        
        for v in set(nodes)-A:

            
            R = set()
            mySum = []
            for R_GX in reachable_nodes_inGX:
            
                for i in nodes:


                    if (i in A) or (i == v):
                        R.update(R_GX[i-1])
                       

                sigma_X = len(R)

                mySum.append(sigma_X)
            
                
            sig_Auv =(1/len(chi)) * sum(mySum)
            sigmas[v] = sig_Auv
        '''   
        for i in A:
                R.update(R_GX[i-1])
                
            for v in nodes:
                if v not in A:
                    
                    R.update(R_GX[v-1])
                    
                    sigma_X = len(R)
                    mySum.append(sigma_X)
    
            
            
                sig_Auv =(1/len(chi)) * sum(mySum)
                sigmas[v] = sig_Auv
            
         
         '''         

        max_sigma = max(sigmas, key = lambda x: sigmas.get(x))
        A.update({max_sigma})
        

    
    #draw graph#
    '''
    plt.subplot(121)
    nx.draw(G,with_labels = True)
    '''

    
            
    return A