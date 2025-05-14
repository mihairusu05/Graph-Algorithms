import heapq
import time

def dijkstra(graph, start_vertex):
    """
    Dijkstra cost walk on a weighted graph
    Time Complexity: O((V + E) log V)
    """
    if not graph.is_weighted:
        raise ValueError("Dijkstra's algorithm requires a weighted graph.")

    distances = {vertex: float('inf') for vertex in graph.return_vertices_list()}
    distances[start_vertex] = 0
    priority_queue = [(0, start_vertex)]
    previous_vertices = {vertex: None for vertex in graph.return_vertices_list()}

    cost_calls = 0
    heap_pushes = 0
    heap_pops = 0

    start_time = time.time()

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        heap_pops += 1

        if current_distance > distances[current_vertex]:
            continue

        for neighbor in graph.neighbours(current_vertex):#Complexity for neighbours->0(v)
            cost_calls += 1
            edge_weight = graph.get_weight(current_vertex, neighbor)#Complexity for get_weight->theta(1)
            distance = current_distance + edge_weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))
                heap_pushes += 1

    end_time = time.time()
    timing = (end_time - start_time) * 1000

    return distances, previous_vertices, timing, cost_calls, heap_pushes, heap_pops



def get_walk(previous_vertices, start_vertex, end_vertex):
    """
    Reconstructs the shortest path from start_vertex to
    end_vertex using the previous_vertices dictionary.
    :param previous_vertices: Dictionary mapping each vertex to its predecessor in the shortest path.
    :param start_vertex:
    :param end_vertex:
    """
    path = []
    current_vertex = end_vertex

    while current_vertex is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]

    if path[0] == start_vertex:
        return path
    else:
        return []


def run_dijkstra_analysis(graph, start_vertex, end_vertex):
    """
    Prints the Dijkstra analysis
    """
    distances, prev, timing, cost_calls, heap_pushes, heap_pops = dijkstra(graph, start_vertex)
    path = get_walk(prev, start_vertex, end_vertex)

    if not path:
        print(f"No valid path found from {start_vertex} to {end_vertex}.")
        return

    print(f"Minimum cost walk from {start_vertex} to {end_vertex}:")
    print(f"Cost: {distances[end_vertex]}")
    print(f"Path: {', '.join(map(str, path))}")
    print(f"Time: {timing:.2f}ms")
    print(f"Calls to cost (g.cost): {cost_calls}")
    print(f"Priority queue operations:")
    print(f"1.heappush (inserts ~ O(log V)): {heap_pushes}")
    print(f"2.heappop (removals ~ O(log V)): {heap_pops}")
