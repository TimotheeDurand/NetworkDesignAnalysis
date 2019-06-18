import networkx as nx
import sys
import numpy as np
from collections import deque

def dualAscent(inputGraph, terminals):
	"""
		Performs dual ascent algorithm on the given graph with the given
		terminals.

		Arguments
		---------
		inputGraph : nx.DiGraph
			directed graph structure containing vertices and weighted arcs
		terminals : list(int)
			list of nodes in the graph that are terminal nodes

		Returns
		-------
		result : (nx.Digraph, nx.Digraph, int, int)
			result of the algorithm containing the different elements:
			- original graph with edge cost updated with reduced costs
			- final saturation graph ($G_A$)
			- root chosen for building the saturation graph
			- lowerbound
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
		visited = np.zeros(graph.number_of_nodes()+1)
		W = [current_terminal]
		fifolist = deque([current_terminal])

		while len(fifolist) > 0 and not rootReached:
			current_node = fifolist.pop()
			visited[current_node] = 1

			for pred in graph_a.predecessors(current_node):
				if(pred == root):
					rootReached = True
					break
				if(visited[pred]==0):
					W.append(pred)
					fifolist.append(pred)

		if rootReached:
			ter = ter[1:]
			continue

		# compute minimum arc going into W
		setIncomingEdges=[]
		minArcWeight = sys.maxsize # delta
		edge_to_add = None
		for u, v, weight in [(u,v,edata['weight']) for u,v,edata in graph.in_edges(nbunch=W, data=True)]:
			if u not in W:		
				if weight < minArcWeight:
					edge_to_add = (u,v)
					minArcWeight = weight
				setIncomingEdges.append((u,v,weight))

		graph_a.add_edge(edge_to_add[0], edge_to_add[1], weight=0)
		
		for u, v, w in setIncomingEdges:
			graph[u][v]['weight'] = min(w-minArcWeight, 0)
		
		lowerBound+=minArcWeight

	return graph, graph_a, root, lowerBound


def primalShortestPathHeuristic(inputGraph, graph_a, terminals, root):
	"""
		Compute a solution to the steiner tree problem using the shortest
		path heuristic (intended to be used on the saturation graph
		returned by the dual ascent algorithm)

		Arguments
		---------
		inputGraph : nx.DiGraph
			directed graph structure containing the original graph
		graph_a : nx.DiGraph
			directed graph structure containing the saturation graph
		terminals : list(int)
			list of nodes in the graph that are terminal nodes
		root : int
			root node from which the path to terminals will be computed
		

		Returns
		-------
		result : (int, list((int, int)))
			result of the algorithm containing the different elements:
			- total cost
			- list of selected edges
	"""
	selectedEdges = set()
	for ter in terminals:
		path = nx.dijkstra_path(graph_a, root, ter)
		for i in range(len(path)-1):
			selectedEdges.add((path[i], path[i+1]))

	sumEdges=0
	for edge in selectedEdges:
		sumEdges+=inputGraph[edge[0]][edge[1]]['weight']

	return sumEdges, selectedEdges
