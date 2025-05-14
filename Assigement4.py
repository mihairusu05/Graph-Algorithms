from domain import SimpleDirectedGraph
import random



def is_connected(graph : SimpleDirectedGraph)->bool:
    """
    A function that checks whether the graph is connected before performing the
    Kruskal's Algorithm
    Complexity : theta(v) - v nr of vertices
    :param graph: `SimpleDirectedGraph`
    :return: `bool`
    """

    if not graph.graph_repo :
        raise ValueError("Graph is empty")
    rand_vertex = random.choice(list(graph.graph_repo.keys()))

    iterator  = graph.bfs_iter(rand_vertex)
    visited_vertices = set()

    for vertex, _ in iterator :
        visited_vertices.add(vertex)

    return len(visited_vertices) == len(graph.graph_repo)

def min_spanning_tree(graph :SimpleDirectedGraph) -> SimpleDirectedGraph :
    """
    Complexity theta (v + e) - v(nr of vertices) , e (nr of edges)
    :param graph:
    :return:
    """
    if graph.is_directed :
        raise ValueError("Kruskal's algorithm requires an undirected graph")
    if not graph.is_weighted :
        raise ValueError("Kruskal's algorithm requires a weighted graph")
    if not is_connected(graph) :
        raise ValueError("Graph should we connected")

    sorted_edges = []
    seen = set()

    for v1 in graph.return_vertices_list() :
        for v2 in graph.neighbours(v1) :
            if (v1, v2) not in seen and (v2, v1) not in seen :
                seen.add((v1, v2))
                weight = graph.get_weight(v1, v2)
                sorted_edges.append((v1, v2, weight))

    sorted_edges.sort(key = lambda x : x[2])

    t = SimpleDirectedGraph()
    t.change_if_weighted()

    for vertex in graph.return_vertices_list() :
        t.add_vertex(vertex)

    forest  = [{v} for v in graph.return_vertices_list()]

    def find_tree(vertex) :
        for tree in forest :
            if vertex in tree :
                return tree
        return None

    def make_union(tree1, tree2) :
        forest.remove(tree1)
        forest.remove(tree2)
        forest.append(tree1.union(tree2))

    i = 0
    while t.get_e() < len(graph.return_vertices_list()) -1 :

        v1, v2, weight = sorted_edges[i]
        tree_of_v1 = find_tree(v1)
        tree_of_v2 = find_tree(v2)

        if tree_of_v1 != tree_of_v2 :
            t.add_edge(v1, v2, weight)
            make_union(tree_of_v1, tree_of_v2)

        i += 1

    return t

def find_all_leaf_nodes(graph : SimpleDirectedGraph)->list :
    """
    A function that uses the DFSIterator to find all leafs
    Complexity : O( v + e)
    :param graph: `SimpleDirectedGRAPH`
    :return: `list`
    """

    root_vertex = '1'
    visited = set()
    parent_map = {}
    child_count = {}

    iterator = graph.dfs_iter(root_vertex)

    for current, _ in iterator :
        visited.add(current)
        child_count[current] = 0
        for neighbour in graph.neighbours(current) :
            if neighbour not in parent_map :
                parent_map[neighbour] = current
                child_count[current] += 1

    leaf_nodes = [node for node in  visited if child_count.get(node, 0) == 0]
    return leaf_nodes



if __name__ == "__main__" :
    graph = SimpleDirectedGraph.create_from_file("input.txt")
    # print(is_connected(graph))

    min_span_tree = min_spanning_tree(graph)
    print("Minimum spanning tree : ")
    print(min_span_tree)
    print("*"*60)
    print("All leafs :")
    print(find_all_leaf_nodes(min_span_tree))

