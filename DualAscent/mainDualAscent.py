import networkx as nx
import time
from algorithmDualAscent import *
from parserSTP import *


# default params
filename = "./testfiles/b18.stp"
dotfile = None
evalMethod = "LazyEval"
helpMsg = """Parameters:
-f [str] : filename
-h [str] : TerminalChoice heuristic {"FullEval" or "LazyEval"}
-d [str] : Output dot file 
-h       : print this help message
"""

# param parsing
params = sys.argv[1:]
while(len(params)>0):
	param = params.pop(0)
	if len(params)>0 and param=="-f":
		filename = params.pop(0)
	elif len(params)>0 and param=="-h":
		timeout = params.pop(0)
	elif len(params)>0 and param=="-d":
		dotfile = params.pop(0)
	elif param=="-h":
		print(helpMsg)
		sys.exit(0)


terminals, graph = parseSTPFile(filename)
t1 = time.time()
newGraph, graph_a, root, lowerBound = dualAscent(graph, terminals, evalMethod)
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


if dotfile != None:
	with open(dotfile, "w") as file:
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
		file.write(dotfile)

