
import random
import networkx as nx
import matplotlib.pyplot as plt
from reachable import reachable_nodes

def cascade(G, A, p):
    
    nodes = list(G)
    edges = G.edges
    
    GX = nx.DiGraph()
    GX.add_nodes_from(nodes)
    
    liveArcs = []
    for edge in edges:
        edgeIsActive = random.random() < p
        if edgeIsActive == True:
            liveArcs.append(edge)
            
    GX.add_edges_from(liveArcs)
    
    
    num_nodes_reached = 0
    for n in A:
        num_nodes_reached = num_nodes_reached + len(reachable_nodes(GX,n))
        


    
    return num_nodes_reached, GX