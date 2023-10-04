from enum import Enum


class Color(Enum):
    WHITE = "white"
    BLACK = "black"
    GREY = "grey"


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Node:
    def __init__(self, name, max_distance, coordinates=None, heuristic=0):
        self._name = name
        self._adjacent = {}
        self._distance = max_distance
        self._visited = False
        self._previous = None
        self._coordinates = coordinates
        self._heuristic = heuristic

    def add_neighbour(self, neighbour, weight=0):
        self._adjacent[neighbour] = weight

    def get_adjacent(self):
        return self._adjacent.items()

    def get_name(self):
        return self._name

    def get_coordinates(self):
        return self._coordinates

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

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    def heuristic(self, h):
        self._heuristic = h

    def get_degree(self):
        return len(self._adjacent)

    def __str__(self):
        return f"Node: {self._name}, Coordinates: {self._coordinates}, Heuristic: {self._heuristic}"

    def __lt__(self, other):
        return (self.distance + self.heuristic) < (other.distance + other.heuristic)
