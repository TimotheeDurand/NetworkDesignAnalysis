import networkx as nx

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
"""