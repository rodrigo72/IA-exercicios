from enum import Enum


class Color(Enum):
    WHITE = "white"
    BLACK = "black"
    GREY = "grey"


class Node:
    def __init__(self, name, max_distance):
        self._name = name
        self._adjacent = {}
        self._distance = max_distance
        self._visited = False
        self._previous = None

    def add_neighbour(self, neighbour, weight=0):
        self._adjacent[neighbour] = weight

    def get_adjacent(self):
        return self._adjacent.items()

    def get_name(self):
        return self._name

    def get_weight(self, neighbour):
        return self._adjacent[neighbour]

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, d):
        self._distance = d

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, v):
        self._visited = v

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, p):
        self._previous = p

    def get_degree(self):
        return len(self._adjacent)

    def __str__(self):
        return str(self._name) + ' adjacent: ' + ', '.join(self._adjacent.keys())

    def __lt__(self, other):
        return self.distance < other.distance
