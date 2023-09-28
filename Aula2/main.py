from graphs import Graph


def main():

    graph = Graph(10000, True)
    graph.add_edge("V1", "V3", 40)
    graph.add_edge("V1", "V2", 70)
    graph.add_edge("V2", "V3", 40)
    graph.add_edge("V2", "V4", 50)
    graph.add_edge("V2", "V5", 60)
    graph.add_edge("V3", "V4", 25)
    graph.add_edge("V4", "V5", 35)
    print(graph.shortest_path("V1", "V5"))  # V1 -> V3 -> V4 -> V5
    print(graph.bfs("V1"))
    print(graph.dfs("V1"))
    print(graph.shortest_path("V3", "V5"))
    graph.draw()


if __name__ == '__main__':
    main()
