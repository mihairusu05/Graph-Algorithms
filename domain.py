import copy
from iterator import DFSIterator,BFSIterator


class SimpleDirectedGraph:
    def __init__(self) -> None:
        """
        Time Complexity: O(1)
        """
        self.graph_repo = {}
        self.graph_weight_repo = {}
        self.is_directed = False
        self.is_weighted = False

    def change_if_directed(self) -> None:
        """
        Changes the graph from directed to undirected and the other way around.
        From undirected to directed an edge becomes double ( A-B) ->(A->B, B->A)
        From directed to undirected (A->B and B->A ) -> (A-B)
        :return : `None`
        Time Complexity: O(V + E)
        """
        self.is_directed = not self.is_directed

        if self.is_directed:

            for vertex in list(self.graph_repo.keys()):
                for neighbor in list(self.graph_repo[vertex]):
                    if vertex not in self.graph_repo[neighbor]:
                        self.graph_repo[neighbor].append(vertex)
                        if self.is_weighted:
                            if neighbor not in self.graph_weight_repo:
                                self.graph_weight_repo[neighbor] = {}
                            #Demo initialization if no data is received from vertex[neighbour]
                            weight = self.graph_weight_repo.get(vertex, {}).get(neighbor, 0)
                            self.graph_weight_repo[neighbor][vertex] = weight
        else:
            for vertex in list(self.graph_repo.keys()):
                for neighbor in list(self.graph_repo[vertex]):
                    if vertex not in self.graph_repo[neighbor]:
                        self.graph_repo[neighbor].append(vertex)
                        if self.is_weighted:
                            if neighbor not in self.graph_weight_repo:
                                self.graph_weight_repo[neighbor] = {}
                            #Same here
                            weight = self.graph_weight_repo.get(vertex, {}).get(neighbor, 0)
                            self.graph_weight_repo[neighbor][vertex] = weight
                # Remove any duplicates from the neighbor list.
                self.graph_repo[vertex] = list(set(self.graph_repo[vertex]))

    def change_if_weighted(self) -> None:
        """
        Sets if the graph is weighted or not.
        :return: `None`
        """
        self.is_weighted = not self.is_weighted

        if self.is_weighted:
            for vertex in list(self.graph_repo.keys()):
                self.graph_weight_repo[vertex] = {}
                for edge in self.graph_repo[vertex]:
                    self.graph_weight_repo[vertex][edge] = 0
        else:
            self.graph_weight_repo.clear()

    def set_weight(self, vertex1, vertex2, weight: int) -> None:
        """
        Sets the weight between two vertices if the graph is weighted.
        In the undirected mode, it updates both directions with the same weight.
        :return:`None`
        """
        if not self.is_weighted:
            raise ValueError("Graph is not weighted!")

        if vertex1 not in self.graph_repo or vertex2 not in self.graph_repo:
            raise ValueError(f"One or both vertices '{vertex1}' and '{vertex2}' are not in the graph.")

        if self.is_directed:
            if vertex2 not in self.graph_repo[vertex1]:
                raise ValueError(f"No edge exists from '{vertex1}' to '{vertex2}'.")

            if vertex1 not in self.graph_weight_repo:
                self.graph_weight_repo[vertex1] = {}
            self.graph_weight_repo[vertex1][vertex2] = weight
        else:
            if (vertex2 not in self.graph_repo[vertex1]) or (vertex1 not in self.graph_repo[vertex2]):
                raise ValueError(f"No edge exists between '{vertex1}' and '{vertex2}'.")
            if vertex1 not in self.graph_weight_repo:
                self.graph_weight_repo[vertex1] = {}
            if vertex2 not in self.graph_weight_repo:
                self.graph_weight_repo[vertex2] = {}
            self.graph_weight_repo[vertex1][vertex2] = weight
            self.graph_weight_repo[vertex2][vertex1] = weight

    def add_vertex(self, vertex_name) -> None:
        """
        Adds a vertex to the graph.
        :return:`None`
        """
        if vertex_name not in self.graph_repo:
            self.graph_repo[vertex_name] = []
            if self.is_weighted :
                self.graph_weight_repo[vertex_name] = {}
        else:
            raise ValueError(f"Vertex '{vertex_name}' already exists in the graph.")

    def add_edge(self, vertex1, vertex2, weight: int = 0) -> None:
        """
        Adds an edge between two vertices.
        If the graph is weighted, the weight is added as well.

        For directed graphs, only a single edge (vertex1 -> vertex2) is added,
        while for undirected graphs the edge is added in both directions.
        :return:`None`
        """
        if vertex1 not in self.graph_repo or vertex2 not in self.graph_repo:
            raise ValueError(
                f"One or both vertices '{vertex1}' and '{vertex2}' are not in the graph."
            )
        #Here I assume that if is directed the order is important as vertex1 being the first vertex
        #And for undirected both should exist and that is why I check only for one

        if vertex2 in self.graph_repo[vertex1]:
            raise ValueError(f"Edge from '{vertex1}' to '{vertex2}' already exists.")

        if self.is_directed:
            self.graph_repo[vertex1].append(vertex2)
            if self.is_weighted:
                if vertex1 not in self.graph_weight_repo:
                    self.graph_weight_repo[vertex1] = {}
                self.graph_weight_repo[vertex1][vertex2] = weight
        else:

            self.graph_repo[vertex1].append(vertex2)
            self.graph_repo[vertex2].append(vertex1)
            if self.is_weighted:
                if vertex1 not in self.graph_weight_repo:
                    self.graph_weight_repo[vertex1] = {}
                if vertex2 not in self.graph_weight_repo:
                    self.graph_weight_repo[vertex2] = {}
                self.graph_weight_repo[vertex1][vertex2] = weight
                self.graph_weight_repo[vertex2][vertex1] = weight

    def get_weight(self, vertex1, vertex2) -> int:
        """
        Returns the weight of an edge given two vertices.
        :return:`int`
        """
        if self.is_edge(vertex1, vertex2) and self.is_weighted:
            return self.graph_weight_repo[vertex1][vertex2]
        else:
            raise ValueError("Attention the graph is either not weighted or the edge does not exist!")

    def remove_edge(self, vertex1, vertex2) -> None:
        """
        Removes an edge between two vertices and updates the weight repository if applicable.
        :return:`None`
        """
        if vertex1 not in self.graph_repo or vertex2 not in self.graph_repo:
            raise ValueError(f"One or both vertices '{vertex1}' and '{vertex2}' are not in the graph.")

        if self.is_directed:
            if vertex2 not in self.graph_repo[vertex1]:
                raise ValueError(f"No edge exists from '{vertex1}' to '{vertex2}'.")
            self.graph_repo[vertex1].remove(vertex2)

            if self.is_weighted and vertex1 in self.graph_weight_repo:
                self.graph_weight_repo[vertex1].pop(vertex2, None)
        else:
            if vertex2 not in self.graph_repo[vertex1] and vertex1 not in self.graph_repo[vertex2]:
                raise ValueError(f"No edge exists between '{vertex1}' and '{vertex2}'.")
            self.graph_repo[vertex1].remove(vertex2)
            self.graph_repo[vertex2].remove(vertex1)
            if self.is_weighted:
                if vertex1 in self.graph_weight_repo:
                    self.graph_weight_repo[vertex1].pop(vertex2, None)
                if vertex2 in self.graph_weight_repo:
                    self.graph_weight_repo[vertex2].pop(vertex1, None)

    def remove_vertex(self, vertex_name) -> None:
        """
        Removes a vertex and all its associated edges. Also cleans up the weight repository.
        :return:`None`
        """
        if vertex_name not in self.graph_repo:
            raise ValueError(f"Vertex '{vertex_name}' not found in the graph.")

        for key in list(self.graph_repo.keys()):
            if vertex_name in self.graph_repo[key]:
                self.graph_repo[key].remove(vertex_name)
                if self.is_weighted and key in self.graph_weight_repo:
                    self.graph_weight_repo[key].pop(vertex_name, None)

        del self.graph_repo[vertex_name]

        if self.is_weighted and vertex_name in self.graph_weight_repo:
            del self.graph_weight_repo[vertex_name]

    def get_v(self) -> int:
        """
        Returns the number of vertices in the graph.
        :return:`int`
        """
        return len(self.graph_repo)

    def get_e(self) -> int:
        """
        Returns the number of edges in the graph.
        :return : `int`
        """
        if self.is_directed:
            return sum(len(neighbors) for neighbors in self.graph_repo.values())
        else:
            return sum(len(neighbors) for neighbors in self.graph_repo.values()) // 2

    def is_edge(self, vertex1, vertex2) -> bool:
        """
        Checks if there is an edge from vertex1 to vertex2.
        :return:`bool`
        """
        if self.is_directed:
            return vertex1 in self.graph_repo and vertex2 in self.graph_repo[vertex1]
        else:
            return (vertex1 in self.graph_repo and vertex2 in self.graph_repo[vertex1] and
                    vertex2 in self.graph_repo and vertex1 in self.graph_repo[vertex2])

    def neighbours(self, vertex_name) -> list:
        """
        Returns a deep copy of all neighbors of a given vertex.
        :return:`list`
        """
        if vertex_name not in self.graph_repo:
            raise ValueError(f"Vertex '{vertex_name}' not found in the graph.")
        return copy.deepcopy(self.graph_repo[vertex_name])

    def inbound_neighbours(self, vertex_name) -> list:
        """
        Returns a list of all inbound neighbors.
        For undirected graphs, this is equivalent to the neighbours.
        :return : `list`
        """
        if self.is_directed:
            if vertex_name not in self.graph_repo:
                raise ValueError(f"Vertex '{vertex_name}' not found in the graph.")
            return [key for key, neighbors in self.graph_repo.items() if vertex_name in neighbors]
        else:
            return self.neighbours(vertex_name)

    def return_vertices_list(self) -> list:
        """
        Returns a list of all vertices.
        :return : `list`
        """
        return list(self.graph_repo.keys())

    def __str__(self) -> str:
        """
        Returns a string representation of the graph.
        :return :`str`
        """
        lines = []
        type_str = ("directed" if self.is_directed else "undirected") + " " + \
                   ("weighted" if self.is_weighted else "unweighted")
        lines.append(type_str)

        printed_edges = set()
        for vertex, neighbors in self.graph_repo.items():
            for neighbor in neighbors:
                if not self.is_directed:
                    edge = tuple(sorted((vertex, neighbor)))
                    if edge in printed_edges:
                        continue
                    printed_edges.add(edge)
                lines.append(f"{vertex} -> {neighbor}")
        for vertex, neighbors in self.graph_repo.items():
            if not neighbors:
                lines.append(f"{vertex}")
        return "\n".join(lines)

    def bfs_iter(self, start_vertex):
        """
        Returns a Breadth-First Search iterator starting from the given vertex.
        """
        if start_vertex not in list(self.graph_repo.keys()) :
            raise ValueError(f"Invalid data for start vertex :{start_vertex}, not part of the graph")
        return BFSIterator(self, start_vertex)

    def dfs_iter(self, start_vertex):
        """
        Returns a Depth-First Search iterator starting from the given vertex.
        """
        if start_vertex not in list(self.graph_repo.keys()) :
            raise ValueError(f"Invalid data for start vertex :{start_vertex}, not part of the graph")
        return DFSIterator(self, start_vertex)

    @classmethod
    def create_from_file(cls, file_path: str) -> "SimpleDirectedGraph":
        """
        Creates a graph from a file with the given format:
        :param file_path: Path to the input file.
        :return: A graph of type SimpleDirectedGraph
        """
        with open(file_path, "r") as file:
            lines = file.readlines()

        graph_type = lines[0].strip().split()
        if len(graph_type) != 2 or graph_type[0] not in {"directed", "undirected"} or graph_type[1] not in {"weighted",
                                                                                                            "unweighted"}:
            raise ValueError("Invalid graph type specification in the first line of the file.")

        is_directed = (graph_type[0] == "directed")
        is_weighted = (graph_type[1] == "weighted")

        graph = cls()
        if is_directed:
            graph.change_if_directed()
        if is_weighted:
            graph.change_if_weighted()

        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) == 1:
                vertex = parts[0]
                if vertex not in graph.graph_repo.keys() :
                    graph.add_vertex(vertex)
            elif len(parts) == 2:
                vertex1, vertex2 = parts
                if vertex1 not in graph.graph_repo.keys() :
                    graph.add_vertex(vertex1)
                if vertex2 not in graph.graph_repo.keys():
                    graph.add_vertex(vertex2)
                if not is_weighted:
                    graph.add_edge(vertex1, vertex2)
                else:
                    raise ValueError(f"Invalid line format: {line.strip()} (expected 3 numbers for a weighted graph)")
            elif len(parts) == 3:
                vertex1, vertex2, weight = parts
                if vertex1 not in graph.graph_repo.keys():
                    graph.add_vertex(vertex1)
                if vertex2 not in graph.graph_repo.keys():
                    graph.add_vertex(vertex2)
                weight = int(weight)
                if is_weighted:
                    graph.add_edge(vertex1, vertex2, weight)
                else:
                    raise ValueError(
                        f"Invalid line format: {line.strip()} (expected 2 numbers for an unweighted graph)")
            else:
                raise ValueError(f"Invalid line format: {line.strip()}")

        return graph


if __name__ == "__main__":
    pass
