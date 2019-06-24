import networkx as nx
import sys
import numpy as np
from collections import deque

def reverseBFS(inputGraph, start, root=None):
	"""
		Performs reverse breadth first search to find the set W
		of nodes reachables from the starting node. If a root node
		is provided (root != None), the search is stopped when the root
		node is reached

		Argument
		--------
		inputGraph : nx.Digraph
			directed graph structure containing vertices and weighted arcs
		start : int
			starting node of the search
		root : int or None
			root node

		Returns
		-------
		result : (set(int), bool)
			result tuple containing the set W and a boolean
			set to true if the root was reached 
	"""

	# perform reverse breadth first search from the current terminal
	# to compute W
	rootReached = False
	visited = np.zeros(inputGraph.number_of_nodes()+1)
	W = [start]
	fifolist = deque([start])

	while len(fifolist) > 0 and not rootReached:
		current_node = fifolist.pop()
		visited[current_node] = 1

		for pred in inputGraph.predecessors(current_node):
			if(pred == root):
				rootReached = True
				W.append(pred)
				fifolist.append(pred)
				break
			if(visited[pred]==0):
				W.append(pred)
				fifolist.append(pred)

	return W, rootReached


def dualAscent(inputGraph, terminals, terminalChoice="LazyEval"):
	"""
		Performs dual ascent algorithm on the given graph with the given
		terminals.

		Arguments
		---------
		inputGraph : nx.DiGraph
			directed graph structure containing vertices and weighted arcs
		terminals : list(int)
			list of nodes in the graph that are terminal nodes
		terminalChoice : str
			technique used for chosing terminal to process
			at each iteration: two possible values:
				- LazyEval
				- FullEval

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

	# we store terminals and their last known value for |W|
	# the list is ordered by ascending value of |W|
	priorityQueue = [[terminal, 1] for terminal in ter]

	# main algo loop
	while len(ter) > 0:

		minSize = 1000000000000000000000000000000
		W = []
		idx = 0

		if terminalChoice == "FullEval":
			# compute each time the BFS for all nodes 
			# to guess the value of |W| for all nodes
			while idx < len(ter):
				W1, rootReached = reverseBFS(graph_a, ter[idx], root)
				if rootReached:
					ter.pop(idx)
					if(len(ter)==0):
						break
					continue
				if len(W1) < minSize:
					minSize = len(W1)
					current_terminal = ter[idx]
					W = W1
				idx+=1

			if(len(ter)==0):
				break
		
		elif terminalChoice == "LazyEval":
			# perform lazy evaluation of the set W reachable by all terminals
			# to chose which terminal to process first; The goal is to process
			# the terminal with a minimal value of |W|.
			W, rootReached = reverseBFS(graph_a, priorityQueue[0][0], root)
			while rootReached:
				priorityQueue.pop(0)
				if len(priorityQueue)==0:
					break
				W, rootReached = reverseBFS(graph_a, priorityQueue[0][0], root)
			if len(priorityQueue)==0:
				break
			if len(priorityQueue)>1:
				W2, rootReached = reverseBFS(graph_a, priorityQueue[1][0], root)
				while rootReached:
					priorityQueue.pop(1)
					if len(priorityQueue)==1:
						break
					W2, rootReached = reverseBFS(graph_a, priorityQueue[1][0], root)

				priorityQueue[0][1]=len(W)

				if(len(priorityQueue)>1):
					priorityQueue[1][1]=len(W2)
					
					if len(W) > len(W2):
						idx=2
						while(idx < len(priorityQueue) and len(W)>priorityQueue[idx][1]):
							idx+=1
						priorityQueue.insert(idx+1, priorityQueue[0])
						priorityQueue.pop(0)
						W = W2

			current_terminal=priorityQueue[0][0]

		else:
			raise Exception("Error: invalid method chosen for terminal choice.")

		# compute minimum arc going into W
		setIncomingEdges=[]
		minArcWeight = sys.maxsize # delta
		for u, v, weight in [(u,v,edata['weight']) for u,v,edata in graph.in_edges(nbunch=W, data=True)]:
			if u not in W:		
				if weight < minArcWeight:
					edge_to_add = (u,v)
					minArcWeight = weight
				setIncomingEdges.append((u,v,weight))
		
		for u, v, w in setIncomingEdges:
			newWeight = w-minArcWeight
			if newWeight < 0:
				newWeight=0
			graph[u][v]['weight'] = newWeight
			if newWeight == 0:
				graph_a.add_edge(u,v, weight=0)
		
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
