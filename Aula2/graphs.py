from nodes import Node
import heapq
from collections import deque


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
        for key in self.nodes_map:
            graph_str += f"{key}: {self.nodes_map[key]}\n"
        return graph_str

    def add_node(self, node):
        self.num_nodes += 1
        new_node = Node(node, self.max_value)
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
        return path

    def bfs(self, start):
        start_node_obj = self.get_node(start)
        if not start_node_obj:
            return None

        path = []
        self._reset_nodes()

        queue = deque()
        queue.append(start_node_obj)
        start_node_obj.visited = True

        while queue:
            current_node = queue.popleft()
            path.append(current_node.get_name())
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
