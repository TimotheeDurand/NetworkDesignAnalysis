import networkx as nx

def parseSTPFile(stpFilePath):
	"""
		Reads a SteinLib file containing an instance of the steiner tree problem (STP).
		The file format is described here: http://steinlib.zib.de/format.php
		The instance is converted into a pair containing a networkx Digraph instance
		and a list of terminal nodes.

		Arguments
		---------

		stpFilePath : str
			Path of the stp file to parse.

		Returns
		-------

		instance : (list(int), nx.DiGraph)
			Parsed instance converted into the a pair containing the following elements:
			- the first element is a list of terminal nodes (each denoted by a string id)
			- the second element is a networkx Digraph structure containing the graph
	"""
	file = open(stpFilePath,"r")

	graph = nx.DiGraph()
	terminals = []

	# format checking
	firstline = file.readline()
	if not firstline.startswith("33D32945"):
		raise Exception('{} is not a proper STP file: does not contain proper first line identifier.'.format(stpFilePath))

	line = file.readline()

	currentSection = ""
	while line:

		if line.startswith("#"):
			continue

		if line.startswith("SECTION "):
			currentSection = line[len("SECTION "):-1]
		elif line.startswith("END"):
			currentSection = ""
		
		if currentSection == "Comment":
			pass
		elif currentSection == "Graph":

			if line.startswith("Nodes "):
				nodeCnt = int(line[len("Nodes "):-1])
				for i in range(1, nodeCnt+1, 1):
					graph.add_node(i)

			elif line.startswith("Edges "):
				edgesCnt = int(line[len("Edges "):-1])
				pass

			elif line.startswith("E "):
				dat = line[len("E "):-1].split()
				n1 = int(dat[0])
				n2 = int(dat[1])
				w = int(dat[2])
				graph.add_edge(n1, n2, weight=w)
				graph.add_edge(n2, n1, weight=w)

		elif currentSection == "Terminals":
			if line.startswith("Terminals "):
				terminalCnt = int(line[len("Terminals "):-1])
				pass
			
			elif line.startswith("T "):
				terminalNr = int(line[len("T "):-1])
				terminals.append(terminalNr)
				graph.node[terminalNr]['color']="red"

		line = file.readline()

	return terminals, graph