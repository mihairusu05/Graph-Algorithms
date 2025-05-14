import heapq
import time

def uniform_cost_search(graph, start_vertex, goal_vertex):
    """
    Uniform Cost Search (UCS) on a weighted graph.
    """
    if not graph.is_weighted:
        raise ValueError("UCS requires a weighted graph.")

    distances = {vertex: float('inf') for vertex in graph.return_vertices_list()}
    distances[start_vertex] = 0
    previous_vertices = {vertex: None for vertex in graph.return_vertices_list()}

    priority_queue = [(0, start_vertex)]

    cost_calls = 0
    heap_pushes = 0
    heap_pops = 0

    start_time = time.time()

    while priority_queue:
        current_cost, current_vertex = heapq.heappop(priority_queue)
        heap_pops += 1

        if current_cost > distances[current_vertex]:
            continue

        # Explore neighbors
        for neighbor in graph.neighbours(current_vertex):
            cost_calls += 1
            edge_weight = graph.get_weight(current_vertex, neighbor)
            new_cost = current_cost + edge_weight

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (new_cost, neighbor))
                heap_pushes += 1

    end_time = time.time()
    timing = (end_time - start_time) * 1000  # Time in milliseconds

    return distances, previous_vertices, timing, cost_calls, heap_pushes, heap_pops

def get_walk(previous_vertices, start_vertex, end_vertex):
    """
    Reconstructs the shortest path from start_vertex to end_vertex
    using the previous_vertices dictionary.
    """
    path = []
    current_vertex = end_vertex

    while current_vertex is not None:
        path.insert(0, current_vertex)
        current_vertex = previous_vertices[current_vertex]

    if path[0] == start_vertex:
        return path
    else:
        return []  # No valid path found

def run_ucs_analysis2(graph, start_vertex, goal_vertex):
    """
    Prints the Uniform Cost Search analysis: shortest path, cost, time, and operations.
    """
    distances, previous_vertices, timing, cost_calls, heap_pushes, heap_pops = uniform_cost_search(graph, start_vertex, goal_vertex)
    path = get_walk(previous_vertices, start_vertex, goal_vertex)

    if not path:
        print(f"No valid path found from {start_vertex} to {goal_vertex}.")
        return

    print(f"Minimum cost walk from {start_vertex} to {goal_vertex}:")
    print(f"Cost: {distances[goal_vertex]}")
    print(f"Path: {', '.join(map(str, path))}")
    print(f"Time: {timing:.2f}ms")
    print(f"Calls to cost (g.cost): {cost_calls}")
    print(f"Priority queue operations:")
    print(f"1.heappush (insertions ~ O(log V)): {heap_pushes}")
    print(f"2.heappop (removals ~ O(log V)): {heap_pops}")

