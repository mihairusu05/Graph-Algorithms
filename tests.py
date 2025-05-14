import unittest
from domain import SimpleDirectedGraph
from iterator import DFSIterator, BFSIterator


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = SimpleDirectedGraph()
        for v in ["1", "2", "3", "4", "5"]:
            self.graph.add_vertex(v)

    def test_add_vertex(self):
        self.graph.add_vertex("6")
        self.assertIn("6", self.graph.graph_repo)

        with self.assertRaises(ValueError):
            self.graph.add_vertex("1")

    def test_add_edge(self):
        self.graph.add_edge("1", "2", 5)
        self.assertIn("2", self.graph.graph_repo["1"])

        with self.assertRaises(ValueError):
            self.graph.add_edge("1", "6", 5)

        self.graph.change_if_weighted()
        self.graph.add_edge("3", "4", 2)
        self.assertEqual(self.graph.get_weight("3", "4"), 2)

    def test_remove_edge(self):
        self.graph.add_edge("1", "2", 5)
        self.graph.remove_edge("1", "2")
        self.assertNotIn("2", self.graph.graph_repo["1"])

        with self.assertRaises(ValueError):
            self.graph.remove_edge("1", "6")

    def test_remove_vertex(self):
        self.graph.add_edge("1", "2", 5)
        self.graph.remove_vertex("1")
        self.assertNotIn("1", self.graph.graph_repo)
        self.assertNotIn("1", self.graph.graph_repo["2"])

        with self.assertRaises(ValueError):
            self.graph.remove_vertex("6")

    def test_bfs_iter(self):
        # Test BFS Iterator functionality
        self.graph.add_edge("1", "2", 5)
        self.graph.add_edge("2", "3", 10)
        self.graph.add_edge("3", "4", 2)

        bfs_iter = self.graph.bfs_iter("1")
        visited = []
        for vertex, distance in bfs_iter:
            visited.append((vertex, distance))

        expected = [("1", 0), ("2", 1), ("3", 2), ("4", 3)]
        self.assertEqual(visited, expected)

        with self.assertRaises(ValueError):
            self.graph.bfs_iter("6")

    def test_dfs_iter(self):
        self.graph.add_edge("1", "2", 5)
        self.graph.add_edge("2", "3", 10)
        self.graph.add_edge("3", "4", 2)

        dfs_iter = self.graph.dfs_iter("1")
        visited = []
        for vertex, depth in dfs_iter:
            visited.append((vertex, depth))

        expected = [("1", 0), ("2", 1), ("3", 2), ("4", 3)]
        self.assertEqual(visited, expected)

        with self.assertRaises(ValueError):
            self.graph.dfs_iter("6")

    def test_change_if_weighted(self):
        self.graph.change_if_weighted()
        self.assertTrue(self.graph.is_weighted)

        self.graph.add_edge("2", "5", 2)
        self.assertEqual(self.graph.get_weight("2", "5"), 2)

        self.graph.change_if_weighted()
        self.assertFalse(self.graph.is_weighted)

    def test_change_if_directed(self):
        self.graph.change_if_directed()
        self.assertTrue(self.graph.is_directed)

        self.graph.add_edge("1", "3", 5)
        self.assertIn("3", self.graph.graph_repo["1"])

        self.graph.change_if_directed()  # Make graph undirected
        self.assertFalse(self.graph.is_directed)

    def test_get_weight(self):
        self.graph.change_if_weighted()
        self.graph.add_edge("1", "2", 5)
        self.assertEqual(self.graph.get_weight("1", "2"), 5)

        self.graph.change_if_weighted()
        with self.assertRaises(ValueError):
            self.graph.get_weight("1", "2")

    def test_return_vertices_list(self):
        self.assertEqual(sorted(self.graph.return_vertices_list()), sorted(["1", "2", "3", "4", "5"]))

    def test_is_edge(self):
        self.graph.add_edge("1", "2", 5)
        self.assertTrue(self.graph.is_edge("1", "2"))
        #The graph is originally undirected so both A-B and B-A exist
        self.assertTrue(self.graph.is_edge("2", "1"))

    def test_graph_from_file(self):
        # Test loading a graph from a file (assumed file format)
        graph = SimpleDirectedGraph.create_from_file("input.txt")

        # Check if vertices and edges are loaded correctly
        self.assertIn("1", graph.graph_repo)
        self.assertIn("2", graph.graph_repo)
        self.assertEqual(graph.get_weight("1", "2"), 5)
        self.assertEqual(graph.get_weight("2", "3"), 10)


if __name__ == "__main__":
    unittest.main()
