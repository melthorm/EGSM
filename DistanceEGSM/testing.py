import sys

def parse_graph(file_path):
    """
    Parse a graph file and return the graph as an adjacency list where each vertex points to a dictionary
    with neighboring vertices and corresponding distances.
    """
    graph = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue  
            parts = line.split()
            if parts[0] == 'v': 
                vertex_id = int(parts[1])
                graph[vertex_id] = {}
            elif parts[0] == 'e': 
                vertex1 = int(parts[1])
                vertex2 = int(parts[2])
                distance = int(parts[3])
                graph[vertex1][vertex2] = distance
                graph[vertex2][vertex1] = distance  
    return graph


def parse_matches(file_path):
    """
    Parse a matches file and return a list of matches where each match is a list of vertex ids.
    """
    matches = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('Match:'):
                match = list(map(int, line.strip().split()[1:]))
                matches.append(match)
 #   print(matches)
    return matches


def check_distances(original_graph, new_graph, match):
    """
    Compare distances in the original graph and new graph based on the matches.
    Print whether the distances match or not.
    """
    
    # Get all distances in new_graph as a list
    new_distances = []
    seen_edges = set()
    for vertex, neighbors in new_graph.items():
        for neighbor, distance in neighbors.items():
            edge = tuple(sorted((vertex,neighbor)))
            if edge not in seen_edges:
                new_distances.append(distance)
                seen_edges.add(edge)
    
    # Match too big
    if (len(match)-1> len(new_distances)):
        print(f"NOT SUCCESSFUL: Match has {len(match)-1} entries, distance has {len(new_distances)} entries")
        return False
    
    original_distances = []
    for i in range(len(match) - 1):
        vertex1, vertex2 = match[i], match[i + 1]
               # print(original_graph)
      #  print(vertex1)
       # print(vertex2)
        distance = original_graph.get(vertex1, {}).get(vertex2)
        if (distance != None):
            original_distances.append(distance)
        else:
            print(f"NOT SUCCESSFUL: Edge {vertex1} - {vertex2} not found in original graph")
            return False
    mapping = lists_equivalent(original_distances, new_distances)
    if (not mapping):
        print("FAIL")
        return False
    print("PASS")
    return True

def lists_equivalent(list1, list2, tolerance=0.3):
    #Sorted lists easier to use
    sorted_list1 = sorted(list1)
    sorted_list2 = sorted(list2)

    if len(sorted_list1) != len(sorted_list2):
        print(f"NOT SUCCESSFUL: Somehow, original_distance length not same as new_distance length")
        return False
    
    # Iterate through all distances of two lsits and compare
    for a, b in zip(sorted_list1, sorted_list2):
        if abs(a - b) > tolerance:
            print(f"NOT SUCCESSFUL: {a} in original_graph and {b} in new_graph not within {tolerance} tolerance")
            return False

    print("SUCCESSFUL: All distances in original graph match distances in new graph.")
    return True

def main():
    if len(sys.argv) != 4:
        print("Usage: python compare_graphs.py <original_graph_file> <new_graph_file> <matches_file>")
        sys.exit(1)

    # File paths
    original_graph_file = sys.argv[1]
    new_graph_file = sys.argv[2]
    matches_file = sys.argv[3]
    
    # Parse the graph files and matches
    original_graph = parse_graph(original_graph_file)
    new_graph = parse_graph(new_graph_file)
    matches = parse_matches(matches_file)
    
    # Check distances
    for match in matches:
        check_distances(original_graph, new_graph, match)


if __name__ == '__main__':
    main()

