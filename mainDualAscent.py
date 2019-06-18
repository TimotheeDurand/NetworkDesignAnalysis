import matplotlib.pyplot as plt
import networkx as nx
from algorithmDualAscent import *
from parserSTP import *

terminals, graph = parseSTPFile("./testfiles/b01.stp")
newGraph, graph_a, root, lowerBound = dualAscent(graph, terminals)
sumEdges, selectedEdges = primalShortestPathHeuristic(graph, graph_a, terminals, root)

print("Lower bound: {}".format(lowerBound))
print("Cost of the solution: {}".format(sumEdges))
print("Selected edges: \n{}".format(selectedEdges))
