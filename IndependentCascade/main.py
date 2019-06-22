from greedy_algorithm import greedy
from parse_snap import myparser
from cascade import cascade
import random
from other_heuristics import out_degree, centrality
import matplotlib.pyplot as plt
import networkx as nx

import time

p = .1
testing_chi_size = 10

out_file = open('testing_results.tsv','w')
out_file.write('Method\tA\tRuntime\tk\tTest\n')

G, nodes, edges = myparser('test_graph1.txt')



for k in [1,2,3,4]:#[1,5,10,15,20]:
        
    for method in ['greedy','random', 'out-degree','closeness centrality']:
    
        
        
        start = time.time()
        if method == 'greedy':
            A = greedy(k,p,10, G,nodes,edges)
 
            

        if method == 'random':
            
            A = set(random.sample(nodes, k))

            
        if method == 'closeness centrality':
            A = centrality(G,k)
            
        if method == 'out-degree':
            A = out_degree(G,k)
        
        end = time.time()
        
        
        #test results#
        nodes_reached= cascade(G,A,p,testing_chi_size)
       
        
        

        out_file.write('%s\t%s\t%f\t%d\t%f\n' %(method, str(A), end - start, k, nodes_reached))

plt.subplot(121)
nx.draw(G,with_labels = True)
    
        
out_file.flush()
out_file.close()
