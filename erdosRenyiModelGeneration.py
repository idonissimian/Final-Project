import numpy as np
from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
import matplotlib.pyplot as plt

# Generate graph
def GenGraph(n, p):
    '''
    # Example: do cycle with rotation - 10
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    G.add_edge(0, 8)
    G.add_edge(1, 4)
    G.add_edge(1, 5)
    G.add_edge(2, 4)
    G.add_edge(2, 8)
    G.add_edge(3, 4)
    G.add_edge(3, 6)
    G.add_edge(3, 7)
    G.add_edge(3, 8)
    G.add_edge(3, 9)
    G.add_edge(4, 5)
    G.add_edge(4, 7)
    G.add_edge(4, 9)
    G.add_edge(5, 8)
    G.add_edge(5, 9)
    G.add_edge(6, 7)
    G.add_edge(6, 8)
    G.add_edge(7, 8)
    G.add_edge(7, 9)
    nx.draw(G, with_labels=True)
    plt.savefig("simple_path.png")
    plt.show()
    return G
    '''

    #Random------------------------
    g = erdos_renyi_graph(n, p)
    print("g.nodes:")
    print(g.nodes)
    print("g.edges:")
    print(g.edges)
    nx.draw(g, with_labels=True)
    plt.savefig("simple_path.png")
    plt.show()
    return g

    '''g.nodes:
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    g.edges:
    [(0, 1), (0, 2), (0, 5), (0, 7), (0, 8), (1, 3), (1, 5), (1, 6), (1, 8), (1, 9), (2, 3), (2, 4), (2, 5), (2, 6), (2, 8), (3, 5), (3, 7), (3, 8), (3, 9), (4, 5), (4, 7), (5, 6), (5, 7), (5, 8), (6, 7), (6, 9), (7, 8)]
    '''
    '''
    #Example: do cycle without rotation - 6
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5])
    G.add_edge(0, 1)
    G.add_edge(0, 3)
    G.add_edge(0, 5)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)
    G.add_edge(2, 4)
    G.add_edge(4, 5)
    nx.draw(G, with_labels=True)
    plt.savefig("simple_path.png")
    plt.show()
    return G
    '''
    '''
    #Example: do cycle without rotation - 10
    G = nx.Graph()
    G.add_nodes_from([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    G.add_edge(0, 4)
    G.add_edge(0, 6)
    G.add_edge(0, 7)
    G.add_edge(0, 9)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 5)
    G.add_edge(1, 6)
    G.add_edge(1, 7)
    G.add_edge(2, 3)
    G.add_edge(2, 5)
    G.add_edge(2, 6)
    G.add_edge(2, 7)
    G.add_edge(3, 4)
    G.add_edge(3, 5)
    G.add_edge(3, 7)
    G.add_edge(4, 6)
    G.add_edge(4, 7)
    G.add_edge(4, 8)
    G.add_edge(5, 6)
    G.add_edge(5, 7)
    G.add_edge(6, 8)
    G.add_edge(6, 9)
    G.add_edge(8, 9)
    nx.draw(G, with_labels=True)
    plt.savefig("simple_path.png")
    plt.show()
    return G
    '''