#parse file

import networkx as nx

def myparser(file_path):
    data = open(file_path, 'r')
    
    
    #######
    #Nodes#
    #######
    
    text = data.readlines()
    
    
    myLine = text[2]
    i = 0
    while i<len(myLine):
        if myLine[:i] == '# Nodes: ':
            numStart = i
        if myLine[i:i+6] == ' Edges':
            numEnd = i
        i += 1
        
    
    numOfNodes = int(myLine[numStart:numEnd])
    nodes = list(range(1,numOfNodes+1))
    
    #######
    #Edges#
    #######
    edges = []
    
    for line in text:
        i = 0
        for char in line:
            if char == '#':
                break
            elif char == '\t':
                fromNode = int(line[0:i])
                toNode = int(line[i+1:len(line)-1])
                edges.append((fromNode,toNode))
            i += 1
        
    
    
    
    G = nx.DiGraph()
    
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    

    
    return G, nodes, edges
    