import random
from collections import defaultdict

from domain import SimpleDirectedGraph
from Assigement4 import is_connected

#Funnction to check whether a graph is Eulerian

def check_if_eul(graph : SimpleDirectedGraph)->bool :
    """
    Checks if a graph is eulerian
    Complexity : Theta(v) v- nr of vertices
    :param graph: `SimpleDirectedGraph`
    :return: `bool`
    """
    if not is_connected(graph) :
        return False
    if graph.is_directed :
        is_eul = True
        for vertex in graph.return_vertices_list() :
            if len(graph.neighbours(vertex)) != len(graph.inbound_neighbours(vertex)) :
                is_eul = False
                break

        return is_eul
    else :
        is_eul = True
        for vertex in graph.return_vertices_list() :
            if len(graph.neighbours(vertex)) % 2 != 0 :
                is_eul = False
                break

        return is_eul



#Function to compute an Eulerian circuit using the Hierholzer algorithm

def get_eul_circuit(graph: SimpleDirectedGraph)->list :
    """
    Function to compute an Eulerian circuit using the Hierholzer algorithm
    :param graph: `SimpleDirectedGraph`
    :return: `list`
    Complexity : theta(v+e)
    """

    if not check_if_eul(graph) :
        return []
    result = []
    neighbours = defaultdict(set)

    for vertex in graph.return_vertices_list() :
        neighbours[vertex] = set()

    for vertex in graph.return_vertices_list() :
        for node in graph.neighbours(vertex) :
            if node not in neighbours[vertex] :
                neighbours[vertex].add(node)
            if not graph.is_directed and vertex not in neighbours[node]:
                neighbours[node].add(vertex)

    start = '6'
    stack = [start]

    while stack :
        current  = stack[-1]
        if neighbours[current] :
            v = random.choice(list(neighbours[current]))
            neighbours[current].remove(v)
            if not graph.is_directed :
                neighbours[v].remove(current)
            stack.append(v)
        else :
            result.append(stack.pop())

    return result[::-1]




if __name__ == "__main__" :
    my_graph = SimpleDirectedGraph.create_from_file('input.txt')

    print(check_if_eul(my_graph))
    print("")
    print(get_eul_circuit(my_graph))