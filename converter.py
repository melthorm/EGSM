## Input File Format
#Both the input query graph and data graph are vertex-labeled. Each graph starts with 't N M' where N is the number of vertices and M is the number of edges. Each vertex is represented by a distinct unsigned integer (from 0 to 4294967295). There is at most one edge between two arbitrary vertices. A vertex and an edge are formatted as `v <vertex-id> <vertex-label> <vertex-degree>` and `e <vertex-id-1> <vertex-id-2>`, respectively. The two endpoints of an edge must appear before the edge. For example, 

'''
t 8 9
v 0 13 3
v 1 0 2
v 2 8 3
v 3 11 4
v 4 9 1
v 5 10 2
v 6 11 2
v 7 3 1
e 0 1
e 0 2
e 0 5
e 1 3
e 2 3
e 2 5
e 3 4
e 3 6
e 6 7
'''

# Take in a networkx file and return a graph file.
import networkx as nx
import matplotlib.pyplot as plt

# Generate a file where each line ends with an attribute.
# v <index> <id> <node_attribute>
# e <start> <end> <edge_attribute>
def gen_all_attr(G, fname='out'):
	# Number of nodes
	N = G.number_of_nodes()
	M = G.number_of_edges()

	nodes = list(G.nodes(data=True))
	edges = list(G.edges(data=True))

	symbol_map = {}
	attribute_mapping = {}
	for node in nodes:
		symbol = node[1]['symbol']
		# Check if symbol is not already in symbol map
		ID = len(symbol_map) 
		if symbol not in symbol_map:
			symbol_map[symbol] = ID
			attribute_mapping[node[0]] = ID
		else:
			attribute_mapping[node[0]] = symbol_map[symbol]

	nx.set_node_attributes(G, attribute_mapping, "id")

	with open(f"{fname}.graph", "w") as f:
		# Write header
		f.write(f"t {N} {M}\n")

		# Write each node
		for n in range(N):
			f.write(f"v {n} {nodes[n][0]} {nodes[n][1]['id']}\n")

		# Write each edge
		for m in range(M):
			f.write(f"e {edges[m][0]} {edges[m][1]} {edges[m][2]['attr']}\n")

	return symbol_map

# Generate a file where each edge line does NOT end with an attribute.
# v <index> <id> <node_attribute>
# e <start> <end>
def gen_no_attr(G, fname='out'):
	# Number of nodes
	N = G.number_of_nodes()
	M = G.number_of_edges()

	nodes = list(G.nodes(data=True))
	edges = list(G.edges(data=True))

	symbol_map = {}
	attribute_mapping = {}
	for node in nodes:
		symbol = node[1]['symbol']
		# Check if symbol is not already in symbol map
		ID = len(symbol_map) 
		if symbol not in symbol_map:
			symbol_map[symbol] = ID
			attribute_mapping[node[0]] = ID
		else:
			attribute_mapping[node[0]] = symbol_map[symbol]

	nx.set_node_attributes(G, attribute_mapping, "id")

	with open(f"{fname}.graph", "w") as f:
		# Write header
		f.write(f"t {N} {M}\n")

		# Write each node
		for n in range(N):
			f.write(f"v {n} {nodes[n][0]} {nodes[n][1]['id']}\n")

		# Write each edge
		for m in range(M):
			f.write(f"e {edges[m][0]} {edges[m][1]}\n")

	return symbol_map

if __name__ == '__main__':
	# Generate graph
	G = nx.balanced_tree(r=3, h=2)
	nx.set_node_attributes(G, {0: "A", 
							   1: "B", 
							   2: "C", 
							   3: "D", 
							   4: "E", 
							   5: "F", 
							   6: "A", 
							   7: "B", 
							   8: "C", 
							   9: "D", 
							   10: "E", 
							   11: "F", 
							   12: "A"}, "symbol")
	nx.set_edge_attributes(G, {(0, 1): 1.0,
							   (0, 2): 2.0,
							   (0, 3): 1.5,
							   (1, 4): 1.6,
							   (1, 5): 1.2,
							   (1, 6): 1.3,
							   (2, 7): 5.2,
							   (2, 8): 2.3,
							   (2, 9): 1.3,
							   (3, 10): 5.5,
							   (3, 11): 6.1,
							   (3, 12): 2.1}, "attr")

	gen_all_attr(G, 'all_attr')
	gen_no_attr(G, 'no_attr')