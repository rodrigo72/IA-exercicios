from graphs import Graph
import math


def heuristic(node, goal):
    if node is None or goal is None:
        return 0

    dx = node.get_coordinates()[0] - goal.get_coordinates()[0]
    dy = node.get_coordinates()[1] - goal.get_coordinates()[1]

    return math.sqrt(dx * dx + dy * dy)


def main():

    graph = Graph(10000, True)
    graph.generate_random_graph(10, 0.22)
    print(graph.shortest_path("V1", "V9"))
    print(graph.astar("V1", "V9", heuristic))
    print(graph)


if __name__ == '__main__':
    main()
