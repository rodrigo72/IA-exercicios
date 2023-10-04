from nodes import Node
import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
import random


class Graph:
    def __init__(self, max_value, is_directed):
        self.nodes_map = {}  # key -> Node
        self.max_value = max_value
        self.is_directed = is_directed
        self.num_nodes = 0

    def __iter__(self):
        return iter(self.nodes_map.values())

    def __str__(self):
        graph_str = ""
        for key, node in self.nodes_map.items():
            graph_str += f"{key}: {node} Coordinates: {node.get_coordinates()}\n"
        return graph_str

    def draw(self):
        if self.is_directed:
            g = nx.DiGraph()
        else:
            g = nx.Graph()

        for node_name, node in self.nodes_map.items():
            g.add_node(node_name)
            for (neighbour, w) in node.get_adjacent():
                g.add_edge(node_name, neighbour.get_name(), weight=w)

        pos = nx.spring_layout(g, k=1.5)

        node_colors = [self.nodes_map[node_name].get_degree() for node_name in g.nodes]
        node_sizes = [200 + 100 * self.nodes_map[node_name].get_degree() for node_name in g.nodes]
        edge_colors = [weight / self.max_value for (_, _, weight) in g.edges(data='weight')]

        plt.figure(figsize=(10, 6))
        nx.draw(
            g,
            pos,
            with_labels=True,
            node_size=node_sizes,
            node_color=node_colors,
            cmap=plt.cm.autumn,
            font_size=10,
            font_color='black',
            font_weight='bold',
            edge_color=edge_colors,
            edge_cmap=plt.cm.autumn,
            width=2,
            arrows=self.is_directed,
        )
        edge_labels = {(node, neighbor): weight for node, neighbor, weight in g.edges(data='weight')}
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=10, font_color='black')

        plt.show()

    def add_node(self, node, coordinates=None):
        self.num_nodes += 1
        new_node = Node(node, self.max_value, coordinates)
        self.nodes_map[node] = new_node
        return new_node

    def get_node(self, node):
        if node in self.nodes_map:
            return self.nodes_map[node]
        else:
            return None

    def add_edge(self, from_node, to_node, weight=0):
        if from_node not in self.nodes_map:
            self.add_node(from_node)
        if to_node not in self.nodes_map:
            self.add_node(to_node)
        self.nodes_map[from_node].add_neighbour(self.nodes_map[to_node], weight)
        if not self.is_directed:  # if undirected
            self.nodes_map[to_node].add_neighbour(self.nodes_map[from_node], weight)

    def get_vertices(self):
        return self.nodes_map.keys()

    def generate_random_graph(self, num_nodes, edge_probability):
        if num_nodes <= 0:
            raise ValueError("Number of nodes must be greater than 0.")
        if edge_probability < 0 or edge_probability > 1:
            raise ValueError("Edge probability must be between 0 and 1.")

        self.nodes_map = {}
        self.num_nodes = 0

        for i in range(num_nodes):
            node_name = f"V{i + 1}"
            self.add_node(node_name, (random.randint(0, 100), random.randint(0, 100)))

        for node1 in self.nodes_map:
            for node2 in self.nodes_map:
                if node1 != node2 and random.random() <= edge_probability:
                    weight = random.randint(1, 100)
                    self.add_edge(node1, node2, weight)

    def _reset_nodes(self):
        for node in self.nodes_map.values():
            node.distance = self.max_value
            node.previous = None
            node.visited = False

    def dijkstra(self, start):

        if start not in self.nodes_map:
            raise ValueError("Start node must exist in the graph.")

        self._reset_nodes()

        start_node_obj = self.nodes_map[start]
        start_node_obj.distance = 0

        priority_queue = [(0, start_node_obj)]

        while priority_queue:
            (current_distance, current_node) = heapq.heappop(priority_queue)
            if not current_node.visited:
                current_node.visited = True
                for (neighbour, weight) in current_node.get_adjacent():
                    if not neighbour.visited:
                        distance = current_distance + weight
                        if distance < neighbour.distance:
                            neighbour.distance = distance
                            neighbour.previous = current_node
                            heapq.heappush(priority_queue, (distance, neighbour))

    def shortest_path(self, start_node, end_node):
        self.dijkstra(start_node)
        path = []
        current = self.nodes_map[end_node]
        while current is not None and current.get_name() != start_node:
            path.insert(0, current.get_name())
            current = current.previous

        if current is not None:
            path.insert(0, current.get_name())
        else:
            path = []

        return path

    def bfs(self, start, end):
        start_node_obj = self.get_node(start)
        if not start_node_obj:
            return None

        path = []
        self._reset_nodes()

        queue = deque()
        queue.append(start_node_obj)
        start_node_obj.visited = True

        path_found = False
        while queue and not path_found:
            current_node = queue.popleft()
            path.append(current_node.get_name())

            if current_node.get_name() == end:
                path_found = True
            else:
                for (neighbour, _) in current_node.get_adjacent():
                    if not neighbour.visited:
                        neighbour.visited = True
                        queue.append(neighbour)

        return path

    def dfs(self, start):
        start_node_obj = self.get_node(start)
        if not start_node_obj:
            return None

        self._reset_nodes()

        def dfs_recursive(node, p):
            node.visited = True
            p.append(node.get_name())

            for (neighbour, _) in node.get_adjacent():
                if not neighbour.visited:
                    dfs_recursive(neighbour, p)

        path = []
        dfs_recursive(start_node_obj, path)
        return path

    # h is the heuristic function. h(n) estimates the cost to reach goal from node n.
    def astar(self, start, goal, h=lambda x, y: 0):
        self._reset_nodes()
        start_node_obj = self.nodes_map[start]
        goal_node_obj = self.nodes_map[goal]

        start_node_obj.heuristic = h(start_node_obj, goal_node_obj)
        open_set = [(0 + start_node_obj.heuristic, start_node_obj)]

        # distance in the class Node serves the role of g_score
        # the sum of distance and heuristic serves the role of f_score

        while open_set:
            current_node = heapq.heappop(open_set)[1]

            if current_node.visited:
                continue
            current_node.visited = True

            if current_node.get_name() == goal:
                path = []
                while current_node:
                    path.insert(0, current_node.get_name())
                    current_node = current_node.previous
                return path

            for (neighbour, weight) in current_node.get_adjacent():
                if not neighbour.visited:
                    tentative_distance = current_node.distance + weight
                    if tentative_distance < neighbour.distance:
                        neighbour.distance = tentative_distance
                        neighbour.previous = current_node
                        neighbour.heuristic = h(neighbour, goal_node_obj)
                        heapq.heappush(open_set, (tentative_distance + neighbour.heuristic, neighbour))

        return None
