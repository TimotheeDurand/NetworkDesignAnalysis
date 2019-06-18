import networkx as nx
import sys

def dualAscent(inputGraph, terminals):
	"""
		performs dual ascent algorithm on the given graph with the given
		terminals.

		Arguments
		---------
		inputGraph : nx.DiGraph
			directed graph structure containing vertices and weighted arcs
		terminals : list(int)
			list of nodes in the graph that are terminal nodes

		Returns
		-------
		result : (nx.Digraph, int, nx.Digraph)
			result of the algorithm containing the different elements:
			- original graph with edge cost updated with reduced costs
			- lowerbound
			- final saturation graph ($G_A$)
	"""

	lowerBound = 0

	# copy input graph to avoid modifying it (we will transform costs into
	# residual costs)
	graph = nx.DiGraph(inputGraph)

	root = terminals[0]
	ter = terminals[1:]

	# initialize graph $G_A$ with nodes but no arc 
	graph_a = nx.DiGraph()
	for node in inputGraph.nodes():
		graph_a.add_node(node)

	# main algo loop
	while len(ter) > 0:
		current_terminal = ter[0]
		
		# perform reverse breadth first search from the current terminal
		# to compute W
		rootReached = False
		W = [current_terminal]
		fifolist = deque([current_terminal])

		while len(fifolist) > 0 and not rootReached:
			current_node = fifolist.pop()

			for pred in graph_a.predecessors(current_node):
				if(pred == root):
					rootReached = True
					break
				W.append(pred)
				fifolist.append(pred)

		if rootReached:
			ter = ter[1:]
			continue

		# compute minimum arc going into W
		setIncomingEdges=[]
		minArcWeight = sys.maxsize # delta
		edge_to_add = None
		for node in W:
			for u, v, weight in [(u,v,edata['weight']) for u,v,edata in G.in_edges(data=True)]:
				if (u not in W):
					edge_to_add = (u,v)
					minArcWeight = weight
				setIncomingEdges.append((u,v,weight))	

		graph_a.add_edge(edge_to_add[0], edge_to_add[1], weight=0)
		for u, v, w in setIncomingEdges:
			graph[u][v]['weight'] = min(w-minArcWeight, 0)
		
		lowerBound+=minArcWeight

	return graph, lowerBound, graph_a
	