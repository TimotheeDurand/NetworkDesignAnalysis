import matplotlib.pyplot as plt
import networkx as nx
import time
from algorithmDualAscent import *
from parserSTP import *

terminals, graph = parseSTPFile("./testfiles/b18.stp")
t1 = time.time()
newGraph, graph_a, root, lowerBound = dualAscent(graph, terminals, "LazyEval")
t2 = time.time()
timeDualAscent = t2 - t1
t1 = time.time()
sumEdges, selectedEdges = primalShortestPathHeuristic(graph, graph_a, terminals, root)
t2 = time.time()
timeShortestPath = t2-t1
print("Lower bound: {}".format(lowerBound))
print("Cost of the solution: {}".format(sumEdges))
print("Selected edges: \n{}".format(selectedEdges))
print("time for dual ascent: {:10.4f}s".format(timeDualAscent))
print("time for shortest path heuristic: {:10.4f}s".format(timeShortestPath))

dotfile = "digraph graphname {\n"
for node in graph_a.nodes():
	dotfile += str(node)
	if node == root:
		dotfile += " [color=red]"
	elif node in terminals:
		dotfile += " [color=blue]"
	dotfile += ";\n"
for u, v in graph.edges():
	dotfile += "{} -> {}[label={},".format(u, v, graph[u][v]["weight"])
	if (u,v) in selectedEdges:
		dotfile += " color=red]".format()
	elif (u,v) in graph_a.edges():
		dotfile += " color=black]".format(graph[u][v]["weight"])
	else:
		dotfile += " color=gray]"
	dotfile += ";\n"
dotfile += "}"
with open("test.dot", "w") as file:
	file.write(dotfile)

