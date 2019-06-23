from greedy_algorithm import greedy
from parse_snap import myparser
from cascade import cascade
import random
from other_heuristics import out_degree, centrality
import matplotlib.pyplot as plt
import networkx as nx

import time

p = .1


out_file = open('results.tsv','w')
out_file.write('Method\tA\tRuntime\tk\tTest\n')

G, nodes, edges = myparser('Wiki-Vote.txt')



for k in [5]:
        
    
    
    for method in ['greedy','random', 'out-degree','closeness centrality']:

        print(str(k))
        start = time.time()
        if method == 'greedy':
           
            A = greedy(k,p,50, G,nodes,edges)

            

 

        if method == 'random':
            
            A = set(random.sample(nodes, k))

            
        if method == 'closeness centrality':
            A = centrality(G,k)
            
        if method == 'out-degree':
            A = out_degree(G,k)
        
        end = time.time()
        
        
        #test results#
        nodes_reached, GX= cascade(G,A,p)
       
        
        out_file.write('%s\t%s\t%f\t%d\t%d\n' %(method, str(A), end - start, k, nodes_reached))


        
out_file.flush()
out_file.close()
