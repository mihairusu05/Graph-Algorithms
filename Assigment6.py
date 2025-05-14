from domain import SimpleDirectedGraph

def find_maximum_cliques_backtracking(graph):
    """
    This algorithm finds all the maximum cliques from a graph
    Complexity : O(2^v * v^2)
    :param graph: `SimpleDirectedGraph`
    :return:
    """
    if graph.is_directed:
        raise ValueError("Clique detection only applies to undirected graphs.")

    vertices = list(graph.return_vertices_list())  # Vertices can be '1', 'apple', 'Zebra', etc.
    max_cliques = []
    max_size = 0

    def is_clique(candidate):
        for i in range(len(candidate)):
            for j in range(i + 1, len(candidate)):
                if candidate[j] not in graph.neighbours(candidate[i]):
                    return False
        return True

    def backtrack(start_index, current):
        nonlocal max_cliques, max_size
        if is_clique(current):
            if len(current) > max_size:
                max_cliques = [current[:]]
                max_size = len(current)
            elif len(current) == max_size:
                max_cliques.append(current[:])

        for i in range(start_index, len(vertices)):
            current.append(vertices[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return max_cliques


if __name__ == "__main__" :
    my_graph = SimpleDirectedGraph.create_from_file('input.txt')

    all_maximum_cliques = find_maximum_cliques_backtracking(my_graph)

    for clique in all_maximum_cliques :
        print(clique)
