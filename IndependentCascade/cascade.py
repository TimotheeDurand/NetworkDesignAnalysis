
import random
import networkx as nx
import matplotlib.pyplot as plt
import statistics

def cascade(G, A, p, chi_size):
    
    nodes = list(G)
    edges = G.edges
    
    GX = nx.DiGraph()
    GX.add_nodes_from(nodes)
    
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
            
    to_average = []
    for X in chi:
            
        GX.add_edges_from(liveArcs)
        
        num_nodes_reached = 0
        for n in A:
            num_nodes_reached = num_nodes_reached + len(nx.algorithms.dag.descendants(GX,n))
        to_average.append(num_nodes_reached)
        
    
    
    
    return statistics.mean(to_average)