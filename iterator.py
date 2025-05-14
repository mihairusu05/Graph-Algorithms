
class BFSIterator:
    def __init__(self, graph, start_vertex):
        if start_vertex not in graph.graph_repo:
            raise ValueError(f"Start vertex '{start_vertex}' is not in the graph.")

        self.graph = graph
        self.queue = [(start_vertex, 0)]
        self.visited = set()
        self.visited.add(start_vertex)
        self.queue_front = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue_front >= len(self.queue):
            raise StopIteration

        current_vertex, current_distance = self.queue[self.queue_front]
        self.queue_front += 1

        for neighbor in self.graph.graph_repo[current_vertex]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.queue.append((neighbor, current_distance + 1))

        return current_vertex, current_distance


class DFSIterator:
    def __init__(self, graph, start_vertex):
        if start_vertex not in graph.graph_repo:
            raise ValueError(f"Start vertex '{start_vertex}' is not in the graph.")

        self.graph = graph
        self.stack = [(start_vertex, 0)]
        self.visited = set()

    def __iter__(self):
        return self

    def __next__(self):

        while self.stack:
            current_vertex, current_depth = self.stack.pop()
            if current_vertex not in self.visited:
                self.visited.add(current_vertex)

                for neighbor in reversed(self.graph.graph_repo[current_vertex]):
                    if neighbor not in self.visited:
                        self.stack.append((neighbor, current_depth + 1))

                return current_vertex, current_depth

        raise StopIteration
