# Course: Data Structures
# Author: Hiromi Watanabe
# Assignment: 6
# Description: This file includes methods related to undirected graphs.
import collections
import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        self.adj_list.setdefault(v, [])
        # self.adj_list[v] = []
        # print(self)
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph. Duplicated elements not allowed.
        """
        if u == v:
            return

        # u and v exist. append the value if it does not exist.
        elif u in self.adj_list and v in self.adj_list:
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)

        # empty case
        elif u not in self.adj_list and v not in self.adj_list:
            self.adj_list[u] = [v]
            self.adj_list[v] = [u]

        # only v exist. create v. append u
        elif u not in self.adj_list and v in self.adj_list:
            self.adj_list[u] = [v]
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)
            else:
                return
        # only u exist. create u. append v
        elif v not in self.adj_list and u in self.adj_list:
            self.adj_list[v] = [u]
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
            else:
                return


    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph. If either (or both) vertex names
        do not exist in the graph, or if there is no edge between them, the
        method does nothing
        """
        if v == u:
            return

        elif u not in self.adj_list and v not in self.adj_list:
            return

        elif u not in self.adj_list:
            return

        elif v not in self.adj_list:
            return

        else:
            l = self.adj_list[u]
            if v in self.adj_list[u]:
                l.remove(v)
            m = self.adj_list[v]
            if u in self.adj_list[v]:
                m.remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        # delete the vertex
        if v in self.adj_list.keys():
            self.adj_list.pop(v)
            # delete connected edges
            for key in self.adj_list:
                if v in self.adj_list[key]:
                    l = self.adj_list[key]
                    l.remove(v)
        else:
            return

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        keys_list = []
        for key in self.adj_list:
            keys_list.append(key)
        return keys_list

    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        keys_list = []
        pair_list = []
        for key in self.adj_list:
            for item in self.adj_list[key]:
                if item not in keys_list:
                    pair_list.append((key,item))
            keys_list.append(key)
        return pair_list

    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise.
        There should not be any restrictions on repetition of vertices/edges.
        """
        if len(path) == 0:
            return True

        if len(path) == 1:
            if path[0] in self.adj_list:
                return True
            else:
                return False

        # 1. check all vertices exist in the path
        for index in range(len(path) - 1):
            if path[index] not in self.adj_list:
                return False
        # 2. check if there is a path exist from one to another
        for i in range(len(path) - 1):
            if path[i + 1] not in self.adj_list[path[i]]:
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        # Initialize an empty set of reachable vertices.
        visited = []
        l = []
        if v_start not in self.adj_list:
            return visited

        # Initialize an empty stack. Add vi to the stack.
        stack = collections.deque([v_start])

        while len(stack) != 0:
            p = stack.pop()
            # the vertex is stored to visited[]
            if p not in visited:
                visited.append(p)
            # store elements in ascending order
                for i in range(len(self.adj_list[p])):
                    l.append(self.adj_list[p][i])
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
        Vertices are picked in alphabetical order
        """
        # Initialize an empty set of reachable vertices.
        visited = []
        l = []
        if v_start not in self.adj_list:
            return visited
        # Initialize an empty queue. Add vi to the stack.
        q = collections.deque([v_start])

        while len(q) != 0:
            p = q.popleft()
            # the vertex is stored to visited[]
            if p not in visited:
                visited.append(p)
                # store elements in ascending order
                for i in range(len(self.adj_list[p])):
                    if self.adj_list[p][i] not in q:
                        l.append(self.adj_list[p][i])
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

    def count_connected_components(self):
        """
        Return number of connected components in the graph
        """
        visited = []
        count = 0

        for i in range(len(self.adj_list)):
            # transform vertex in list form
            vertex_list = list(self.adj_list)
            # visited vertex from dfs method is returned and add 1 to count
            if vertex_list[i] not in visited:
                vertices = self.dfs(vertex_list[i])
                count += 1
                # visited vertex is stored to visited
                if len(vertices) > 0:
                    for j in range(len(vertices)):
                        if vertices[j] not in visited:
                            visited.append(vertices[j])
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        # Initialize an empty set of reachable vertices.
        visited = []

        # Initialize an empty stack. Add vi to the stack.
        vertices = list(self.adj_list.keys())

        # To be sure we check every single vertex.
        for m in range(len(vertices) - 1):
            # check that vertex has neighbors
            if len(self.adj_list[vertices[m]]) != 0:
                stack = collections.deque(vertices[m])
                # keep track of parents (at first we can pass whatever we want)
                parent_s = collections.deque('a')

                while len(stack) != 0:
                    p = stack.pop()
                    parent = parent_s.pop()
                    # the vertex is stored to visited[]
                    if p not in visited:
                        visited.append(p)

                        for i in range(len(self.adj_list[p])):
                            if self.adj_list[p][i] not in visited:
                                stack.append(self.adj_list[p][i])
                                parent_s.append(p)
                            # check if the destination is already where it's been visited
                            # and also it is not parent
                            elif self.adj_list[p][i] in visited and self.adj_list[p][i] != parent and self.adj_list[p][i] != 'a':
                                return True
        return False


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)
    #
    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)
    #
    # g.add_vertex('A')
    # print(g)
    # for u, v in ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']:
    # # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)
    #
    #
    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)

    #
    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # # test_cases = ['ECABDCBE']
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # print(g.bfs('A', 'Q'))
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')
    #

    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    edges = ['FC', 'FJ', 'CF', 'CK', 'HI', 'HB', 'HE', 'IH', 'IB', 'IA', 'BI', 'BH', 'EH',  'AI']
    g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    print(g)
        # print('{:<10}'.format(case), g.has_cycle())
    print(g.has_cycle())
