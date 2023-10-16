import heapq
import math
from queue import Queue

import networkx as nx
import matplotlib.pyplot as plt  # idem

from Nodo import Node


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()
    return total_path


class Graph:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}
        self.m_h = {}

    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out

    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
        return None

    def print_edge(self):
        list_a = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, cost) in self.m_graph[nodo]:
                list_a = list_a + nodo + " ->" + nodo2 + " cost:" + str(cost) + "\n"
        return list_a

    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if n1 not in self.m_nodes:
            n1_id = len(self.m_nodes)
            n1.set_id(n1_id)
            self.m_nodes.append(n1)
            self.m_graph[node1] = []

        if n2 not in self.m_nodes:
            n2_id = len(self.m_nodes)
            n2.set_id(n2_id)
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        self.m_graph[node1].append((node2, weight))

        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    def get_nodes(self):
        return self.m_nodes

    def draw(self):
        lista_v = self.m_nodes
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.get_name()
            g.add_node(n)
            for (adjacent, peso) in self.m_graph[n]:
                g.add_edge(n, adjacent, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def get_arc_cost(self, node1, node2):
        cost_t = math.inf
        a = self.m_graph[node1]
        for (node, cost) in a:
            if node == node2:
                cost_t = cost

        return cost_t

    def calculate_cost(self, path):
        test = path
        cost = 0
        i = 0
        while i + 1 < len(test):
            cost = cost + self.get_arc_cost(test[i], test[i + 1])
            i = i + 1
        return cost

    def dfs(self, start, end, path=None, visited=None):
        if visited is None:
            visited = set()

        if path is None:
            path = []

        path.append(start)
        visited.add(start)

        if start == end:
            cost_t = self.calculate_cost(path)
            return path, cost_t

        for (adjacent, peso) in self.m_graph[start]:
            if adjacent not in visited:
                result = self.dfs(adjacent, end, path, visited)
                if result is not None:
                    return result
        path.pop()
        return None

    def bfs(self, start, end):

        visited = set()
        fila = Queue()
        cost = 0

        fila.put(start)
        visited.add(start)

        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and not path_found:
            current_node = fila.get()
            if current_node == end:
                path_found = True
            else:
                for (adjacent, peso) in self.m_graph[current_node]:
                    if adjacent not in visited:
                        fila.put(adjacent)
                        parent[adjacent] = current_node
                        visited.add(adjacent)

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            cost = self.calculate_cost(path)
        return path, cost

    def add_heuristic(self, n, estimate):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = estimate

    def get_h(self, n):
        return self.m_h[n]

    def get_neighbours(self, n):
        return self.m_graph[n]

    # goal is: Lisbon (heuristics are based on this goal)
    # finds a path from start to goal using A* search
    def astar(self, start, end):

        if start not in self.m_graph.keys() or end not in self.m_graph.keys():
            return None

        # The set of discovered nodes that may need to be (re-)expanded.
        # Initially, only the start node is known.
        # This is usually implemented as a min-heap or priority queue rather than a hash-set.
        open_set = [(0, start)]

        # For node n, came_from[n] is the node immediately preceding it on the cheapest path from start to n
        # currently known.
        came_from = {}

        # For node n, g_score[n] is the cost of the *cheapest path from start to n* currently known.
        g_score = {node.get_name(): float("inf") for node in self.m_nodes}
        g_score[start] = 0

        # For node n, f_score[n] := g_score[n] + h(n). f_score[n] represents our current best guess as to
        # how cheap a path could be from start to finish if it goes through n.
        f_score = {node.get_name(): float("inf") for node in self.m_nodes}
        f_score[start] = g_score[start] + self.get_h(start)  # <=> 0 + self.get_h(start)

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == end:
                path = reconstruct_path(came_from, current)
                return path, g_score[current]

            for (neighbor, weight) in self.m_graph[current]:
                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_g_score is the distance from start to the neighbor through current

                tentative_g_score = g_score[current] + weight

                if tentative_g_score < g_score[neighbor]:
                    # This path to neighbor is better than any previous one
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.get_h(neighbor)
                    if neighbor not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    # dijkstra's algorithm
    def greedy(self, start, end):

        if start not in self.m_graph.keys() or end not in self.m_graph.keys():
            return None

        open_set = [(0, start)]
        visited = set()
        came_from = {}
        score = {node.get_name(): float("inf") for node in self.m_nodes}

        while open_set:
            (current_score, current_node) = heapq.heappop(open_set)

            if current_node == end:
                path = reconstruct_path(came_from, current_node)
                return path, score[current_node]

            if current_node not in visited:
                visited.add(current_node)
                for (neighbour, weight) in self.m_graph[current_node]:
                    if neighbour not in visited:
                        tentative_score = current_score + weight
                        if tentative_score < score[neighbour]:
                            score[neighbour] = tentative_score
                            came_from[neighbour] = current_node
                            heapq.heappush(open_set, (score[neighbour], neighbour))

        return None
