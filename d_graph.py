# Course: CS261 - Data Structures
# Author: Hiromi Watanabe
# Assignment: 6
# Description: This file includes methods related to directed graphs.

import collections
import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Add new vertex to the graph and returns the number of vertices in the graph after the addition.
        """
        self.adj_matrix = [[0 for column in range(self.v_count + 1)] for row in range(self.v_count + 1)]
        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add edge to the graph. Duplicated elements not allowed.
        """
        if not (0 <= src < self.v_count and 0 <= dst < self.v_count):
            return
        elif weight < 0 or src == dst:
            return
        else:
            self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method removes an edge between two vertices with provided indices.
        """
        if not (0 <= src < self.v_count and 0 <= dst < self.v_count):
            return
        elif self.adj_matrix[src][dst] == 0:
            return
        else:
            self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph
        """
        v = []
        for i in range(self.v_count):
            v.append(i)
        return v

    def get_edges(self) -> []:
        """
        Return list of edges in the graph
        """
        edges = []
        for i in range(len(self.adj_matrix)):
            for j in range(len(self.adj_matrix[i])):
                if self.adj_matrix[i][j] != 0 and (i and j) >= 0:
                    edges.append((i, j, self.adj_matrix[i][j]))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        This method takes a list of vertex indices and returns True
        if the sequence of vertices represents a valid path in the graph.
        Algorithm: see if one vertex to another has weight edge or not.
        """
        if len(path) == 0 or len(path) == 1:
            return True
        else:
            for i in range(len(path) - 1):
                if self.adj_matrix[path[i]][path[i + 1]] == 0:
                    return False
            return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in ascending order
        """
        # Initialize an empty set of reachable vertices.
        visited = []
        l = []
        if not 0 <= v_start < self.v_count:
            return visited

        # Initialize an empty stack. Add vi to the stack.
        stack = collections.deque([v_start])

        while len(stack) != 0:
            p = stack.pop()
            # the vertex is stored to visited[]
            if p not in visited:
                visited.append(p)
                # store elements in ascending order
                for i in range(len(self.adj_matrix[p])):
                    if self.adj_matrix[p][i] != 0:
                        l.append(i)
                sorted_l = sorted(l)
                # reset the list
                l = []
                # append sorted list to stack in backwards (so that it pops in ascending order)
                for j in range(len(sorted_l) - 1, -1, -1):
                    stack.append(sorted_l[j])
                # return if it reached the v_end
                if p == v_end:
                    return visited
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in ascending order
        """
        # Initialize an empty set of reachable vertices.
        visited = []
        l = []
        if not 0 <= v_start < self.v_count:
            return visited
        # Initialize an empty queue. Add vi to the stack.
        q = collections.deque([v_start])

        while len(q) != 0:
            p = q.popleft()
            # the vertex is stored to visited[]
            if p not in visited:
                visited.append(p)
                # store elements in ascending order
                for i in range(len(self.adj_matrix[p])):
                    if self.adj_matrix[p][i] != 0 and i not in q:
                        l.append(i)
                sorted_l = sorted(l)
                # reset the list
                l = []
                # append sorted list to queue in ascending order)
                for j in range(len(sorted_l)):
                    q.append(sorted_l[j])
                # return if it reached the v_end
                if p == v_end:
                    return visited
        return visited

    def has_cycle(self):
        """
        Returns true when there is a cycle in a graph.
        """
        # for every vertex, call dfs.
        for idx in range(self.v_count - 1):
            for i in self.dfs(idx):
                # for every vertex pair inside of vertex i, if it is flipped, it indicates the cycle
                if self.adj_matrix[i][idx] > 0:
                    return True
        return False

    def dijkstra(self, src: int) -> []:
        """
        Returns the shortest path to from each vertex to the starting vertex.
        """
        vertices = self.get_vertices()
        visited = []
        dist = {}
        parent = {}
        neighbors = {}
        # 1. assign inf to each vertex except starting vertex has 0
        for i in vertices:
            dist[i] = float('inf')
            parent[i] = None
            # visited.append(i)
        dist[src] = 0
        # 2. find neighbors for each vertex
        for j in vertices:
            neighbors[j] = []
            for k in range(len(self.adj_matrix[j])):
                if self.adj_matrix[j][k] != 0 and (j and k) >= 0:
                    neighbors[j].append(k)
        # 3. count with the lowest cost to the starting vertex until vertices are empty
        idx = src
        while len(vertices) != 0:
            for vertex in vertices:
                if dist[idx] > dist[vertex]:
                    idx = vertex
            vertices.remove(idx)

            for v in neighbors[idx]:
                if v in vertices:
                    path = self.adj_matrix[idx][v] + dist[idx]
                    if path < dist[v]:
                        dist[v] = path
                        parent[v] = idx

            if len(vertices) > 0:
                idx = vertices[0]

        dijkstra = []
        for d in dist.values():
            dijkstra += [d]
        return dijkstra







if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)
    #
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)

    # print("\nPDF - method add_vertex() / add_edge example 1.5")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # g.remove_edge(6, 9)
    # print(g)

    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    #

    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    # print("\nPDF - dijkstra() example 1")
    # print("--------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    # g.remove_edge(4, 3)
    # print('\n', g)
    # for i in range(5):
    #     print(f'DIJKSTRA {i} {g.dijkstra(i)}')
