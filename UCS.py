import heapq
import time

def uniform_cost_search(graph, start, goal=None):
    """
    Uniform Cost Search walk on a weighted graph.
    Stops early if goal is reached.
    O((V+E)logV)
    """
    distance = {v: float('inf') for v in graph.graph_repo}
    previous = {v: None for v in graph.graph_repo}

    distance[start] = 0
    pq = []
    heapq.heappush(pq, (0, start))

    cost_calls = 0
    heap_pushes = 1
    heap_pops = 0

    start_time = time.time()

    while pq:
        current_dist, current_node = heapq.heappop(pq)
        heap_pops += 1

        if goal is not None and current_node == goal:
            break

        for neighbor, weight in graph.graph_weight_repo[current_node].items():
            cost_calls += 1
            new_dist = current_dist + weight

            if new_dist < distance[neighbor]:
                distance[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))
                heap_pushes += 1

    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # in milliseconds

    return distance, previous, execution_time, cost_calls, heap_pushes, heap_pops


def get_walk(previous_vertices, start_vertex, end_vertex):
    """
    Reconstructs the shortest path from start_vertex to end_vertex using the 'previous' map.

    :param previous_vertices: Dictionary that maps each vertex
    to its predecessor in the shortest path.
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


def run_ucs_analysis(graph, start_vertex, end_vertex):
    """
    Prints the UCS analysis
    """
    distances, previous, timing, cost_calls, heap_pushes, heap_pops = uniform_cost_search(graph, start_vertex)
    path = get_walk(previous, start_vertex, end_vertex)

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
