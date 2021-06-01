import sys
import networkx as nx
# import matplotlib.pyplot as plt
import posa_improvement_for_geometric_model
import posa_algorithm
# import geometric_model_generation
import pandas as pd

'''import posaWithNetworkClass
import erdosRenyiNetwork
import Point as Pnt
import random as rd
import Edge as Edg
import erdosRenyiModelGeneration
import geometricModelGeneration'''

'''
#Run posa on our erdos renyi network
er_net = erdosRenyiNetwork.Network()
n = 20
for i in range(0, n):
    p = pnt.Point(i)
    er_net.add_vertex(p)
for i in range(0, n):
    num = round(rd.uniform(0, n))
    for j in range(0, num):
        if i != j:
            er_net.add_edge_by_vtx(er_net.nodes[i], er_net.nodes[j])
er_net.draw_network()
rail_v, rail_e = posaWithNetworkClass.posa(er_net)
'''
# =================================================
'''
n = 20
r = 0.9
# g = erdosRenyiModelGeneration.gen_graph(n, p)
# rail_v_gnp, rail_e_gnp = posaAlgorithm.posa(g)
g = geometric_model_generation.gen_graph(n, r)
print("Posa improvement :")
rail_v_geo, rail_e_geo = posa_improvement_for_geometric_model.posa(g)
print("len of rail :", len(rail_v_geo))
if len(rail_e_geo) == n:
    print("Found hamiltonian cycle")
else:
    print("Didn't find hamiltonian cycle")
'''
# =================================================
'''# Run posa on gnp
col_names = ['n', 'p', 'len_of_rail', 'is_found_hamilton_cycle']
exp_df = pd.DataFrame(columns=col_names)
n_list = [20, 50, 70, 100, 150, 200]
p_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for n in n_list:
    for p in p_list:
        try:
            g = nx.erdos_renyi_graph(n, p)
            rail_v, rail_e = posa_algorithm.posa(g)
            print("len of rail :", len(rail_v))
            if len(rail_e) == n:
                print("Found hamiltonian cycle")
                df_i = pd.DataFrame([[n, p, len(rail_v), 'V']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
            else:
                print("Didn't find hamiltonian cycle")
                df_i = pd.DataFrame([[n, p, len(rail_v), 'X']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
        except:
            print("Didn't find hamiltonian cycle")
            len_of_rail = sys.exc_info()[1]
            df_i = pd.DataFrame([[n, p, len_of_rail, 'X']], columns=col_names)
            exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
exp_df.to_csv('posa_gnp.csv')'''
# =================================================
'''# Run posa on barabasi
col_names = ['n', 'm', 'len_of_rail', 'is_found_hamilton_cycle']
exp_df = pd.DataFrame(columns=col_names)
n_list = [20,50,70,100,150,200]
m_list = [1,2,3,4,5,6,7,8,9]
for n in n_list:
    for m in m_list:
        try:
            g = nx.barabasi_albert_graph(n, m)
            rail_v, rail_e = posa_algorithm.posa(g)
            print("len of rail :", len(rail_v))
            if len(rail_e) == n:
                print("Found hamiltonian cycle")
                df_i = pd.DataFrame([[n, m, len(rail_v), 'V']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
            else:
                print("Didn't find hamiltonian cycle")
                df_i = pd.DataFrame([[n, m, len(rail_v), 'X']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
        except:
            print("Didn't find hamiltonian cycle")
            len_of_rail = sys.exc_info()[1]
            df_i = pd.DataFrame([[n, m, len_of_rail, 'X']], columns=col_names)
            exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
exp_df.to_csv('posa_barabasi.csv')'''
# =================================================
'''# Run posa on gnr
col_names = ['n', 'r', 'len_of_rail', 'is_found_hamilton_cycle']
exp_df = pd.DataFrame(columns=col_names)
n_list = [20, 50, 70, 100, 150, 200]
r_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for n in n_list:
    for r in r_list:
        try:
            g = nx.random_geometric_graph(n, r)
            rail_v, rail_e = posa_algorithm.posa(g)
            print("len of rail :", len(rail_v))
            if len(rail_e) == n:
                print("Found hamiltonian cycle")
                df_i = pd.DataFrame([[n, r, len(rail_v), 'V']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
            else:
                print("Didn't find hamiltonian cycle")
                df_i = pd.DataFrame([[n, r, len(rail_v), 'X']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
        except:
            print("Didn't find hamiltonian cycle")
            len_of_rail = sys.exc_info()[1]
            df_i = pd.DataFrame([[n, r, len_of_rail, 'X']], columns=col_names)
            exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
exp_df.to_csv('posa_gnr.csv')'''
# =================================================
'''# Run posa on gnr
col_names = ['n', 'r', 'len_of_rail', 'is_found_hamilton_cycle']
exp_df = pd.DataFrame(columns=col_names)
n_list = [20, 50, 70, 100, 150, 200]
r_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for n in n_list:
    for r in r_list:
        try:
            g = nx.random_geometric_graph(n, r)
            rail_v, rail_e = posa_improvement_for_geometric_model.posa(g)
            print("len of rail :", len(rail_v))
            if len(rail_e) == n:
                print("Found hamiltonian cycle")
                df_i = pd.DataFrame([[n, r, len(rail_v), 'V']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
            else:
                print("Didn't find hamiltonian cycle")
                df_i = pd.DataFrame([[n, r, len(rail_v), 'X']], columns=col_names)
                exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
        except:
            print("Didn't find hamiltonian cycle")
            len_of_rail = sys.exc_info()[1]
            df_i = pd.DataFrame([[n, r, len_of_rail, 'X']], columns=col_names)
            exp_df = exp_df.append(df_i, ignore_index=True, sort=False)
exp_df.to_csv('posa_improvement_gnr_3.csv')'''
# =================================================
'''# I-M-P-O-R-T-A-N-T : case that Posa regular failed and Posa improve succeeds
g = nx.Graph()
g.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
g.add_edge(1, 2)
g.add_edge(2, 3)
g.add_edge(3, 4)
g.add_edge(4, 5)
g.add_edge(5, 6)
g.add_edge(1, 7)
g.add_edge(2, 7)
g.add_edge(1, 8)
g.add_edge(2, 8)
g.add_edge(7, 11)
g.add_edge(8, 11)
g.add_edge(9, 11)
g.add_edge(10, 11)
g.add_edge(2, 11)
g.add_edge(4, 9)
g.add_edge(5, 9)
g.add_edge(5, 10)
g.add_edge(6, 10)

# rail_v = [1,2,3,4,5,6]
# rail_e = [(1,2),(2,3),(3,4),(4,5),(5,6)]
# rail_v, rail_e = posaImprovementForGeometricModel.absorb_vertices(g, rail_v, rail_e)
# rail_v, rail_e = posa_algorithm.posa(g)
rail_v, rail_e = posa_improvement_for_geometric_model.posa(g)
pos = nx.spring_layout(g)
# nx.draw(g, with_labels=True)
nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap('jet'), node_size=500)
nx.draw_networkx_labels(g, pos)
nx.draw_networkx_edges(g, pos, edgelist=g.edges, edge_color='k', arrows=True)
nx.draw_networkx_edges(g, pos, edgelist=rail_e, edge_color='r', arrows=True)
plt.savefig("posa_path_improvement_drawing.png")
plt.show()'''

'''G = nx.random_geometric_graph(6, 0.5)
edge_x = []
edge_y = []
for edge in G.edges():
    print("edge[0]")
    print(edge[0])
    print("edge[1]")
    print(edge[1])
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    print("x0")
    print(x0)
    print("y0")
    print(y0)
    print("x1")
    print(x1)
    print("y1")
    print(y1)
nx.draw(G, with_labels=True)
plt.savefig("simple_path.png")
plt.show()'''
