from Grafo import Graph


def main():
    g = Graph()

    g.add_edge("elvas", "borba", 15)
    g.add_edge("borba", "estremoz", 15)
    g.add_edge("estremoz", "evora", 40)
    g.add_edge("evora", "montemor", 20)
    g.add_edge("montemor", "vendasnovas", 15)
    g.add_edge("vendasnovas", "lisboa", 50)
    g.add_edge("elvas", "arraiolos", 50)
    g.add_edge("arraiolos", "alcacer", 90)
    g.add_edge("alcacer", "palmela", 35)
    g.add_edge("palmela", "almada", 25)
    g.add_edge("palmela", "barreiro", 25)
    g.add_edge("barreiro", "palmela", 30)
    g.add_edge("almada", "lisboa", 15)
    g.add_edge("elvas", "alandroal", 40)
    g.add_edge("alandroal", "redondo", 25)
    g.add_edge("redondo", "monsaraz", 30)
    g.add_edge("monsaraz", "barreiro", 120)
    g.add_edge("barreiro", "baixadabanheira", 5)
    g.add_edge("baixadabanheira", "moita", 7)
    g.add_edge("moita", "alcochete", 20)
    g.add_edge("alcochete", "lisboa", 20)

    g.add_heuristic("elvas", 270)
    g.add_heuristic("borba", 250)
    g.add_heuristic("estremoz", 145)
    g.add_heuristic("evora", 95)
    g.add_heuristic("montemor", 70)
    g.add_heuristic("vendasnovas", 45)
    g.add_heuristic("arraiolos", 220)
    g.add_heuristic("alcacer", 140)
    g.add_heuristic("palmela", 85)
    g.add_heuristic("almada", 25)
    g.add_heuristic("alandroal", 180)
    g.add_heuristic("redondo", 170)
    g.add_heuristic("monsaraz", 120)
    g.add_heuristic("barreiro", 30)
    g.add_heuristic("baixadabanheira", 33)
    g.add_heuristic("moita", 35)
    g.add_heuristic("alcochete", 26)
    g.add_heuristic("lisboa", 0)

    saida = -1
    while saida != 0:
        print("1-Imprimir Grafo")
        print("2-Desenhar Grafo")
        print("3-Imprimir  nodos de Grafo")
        print("4-Imprimir arestas de Grafo")
        print("5-DFS")
        print("6-BFS")
        print("7-A*")
        print("8-Gulosa")
        print("0-Saír")

        saida = -1

        try:
            saida = int(input("introduza a sua opcao-> "))
        except ValueError:
            print("Introduza um numero")

        if saida == 0:
            print("saindo.......")
        elif saida == 1:
            print(g.m_graph)
            input("prima enter para continuar")
        elif saida == 2:
            g.draw()
        elif saida == 3:
            print(g.m_graph.keys())
            input("prima enter para continuar")
        elif saida == 4:
            print(g.print_edge())
            input("prima enter para continuar")
        elif saida == 5:
            start = input("Nodo inicial->")
            goal = input("Nodo final->")
            print(g.dfs(start, goal, path=[], visited=set()))
            input("prima enter para continuar")
        elif saida == 6:
            start = input("Nodo inicial->")
            goal = input("Nodo final->")
            print(g.bfs(start, goal))
            input("prima enter para continuar")
        elif saida == 7:
            start = input("Nodo inicial->")
            goal = input("Nodo final->")
            print(g.astar(start, goal))
            input("prima enter para continuar")
        elif saida == 8:
            start = input("Nodo inicial->")
            goal = input("Nodo final->")
            print(g.greedy(start, goal))
            input("prima enter para continuar")


if __name__ == "__main__":
    main()
