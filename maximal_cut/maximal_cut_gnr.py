import point as pnt
import geometric_network as ge_net
import numpy as np
import math


# -----------------------------------------------------------------------------------------------------
# Definition of class represents circle

class Circle:
    r: int = 0
    center_x: float = 0.0
    center_y: float = 0.0

    def __init__(self, rad: int, p: pnt):
        self.r = rad
        self.center_x = p.x_value
        self.center_y = p.y_value

    def calculate_relation_to_circle(self, vtx: pnt):
        val = (vtx.x_value - self.center_x) ** 2 + (vtx.y_value - self.center_y) ** 2 - self.r ** 2
        return val

    def print_line(self):
        print("(x -", self.center_x, ")² + (y -", self.center_y, ")² =", self.r ** 2)


# -----------------------------------------------------------------------------------------------------

def generate_model(n, r):
    net = ge_net.Network(r)
    for i in range(0, n):
        p = pnt.Point(i)
        net.add_vertex(p)
    net.make_edges()
    net.print_network()
    net.draw_network("main_network")
    return net


# -----------------------------------------------------------------------------------------------------
# Calculate nodes degree and return a sorted list with the degrees
# In addition the function return list with nodes number where in the start of the list exist the most connected node

def cal_sort_nodes_by_degree(net):
    degree_list = []
    # Get the adjacency matrix
    mat = net.adjacency_matrix()
    n = len(mat)
    # print("mat :")
    # net.print_mat(mat)
    # Create list of degrees by the adjacency matrix
    for i in range(n):
        degree_list.append(sum(mat[i]))
    # print("degree_list :", degree_list)
    # Sort the nodes by degree
    indexes_list = list(np.arange(n))
    zipped_lists = zip(degree_list, indexes_list)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    degree_list, indexes_list = [list(t) for t in tuples]
    print("degree_list :", degree_list)
    print("indexes_list :", indexes_list)
    return degree_list, indexes_list


# -----------------------------------------------------------------------------------------------------
# Recursion function : Update S and T - create the maximal cut

def divide_to_groups(net, len_of_cut, set_s_centers, set_t, degree_list, indexes_list, nodes_number_list):
    # k is ceiling value of lan(n)
    k = math.ceil(math.log(len(indexes_list)))
    if k == 0:
        k = 1
    k_high_deg_nodes_num = indexes_list[0:k]
    # print("k :", k)
    # print("k_high_deg_nodes_num :")
    # print(k_high_deg_nodes_num)
    for node_number_i in k_high_deg_nodes_num:
        # Insert the center nodes into set_s_centers
        set_s_centers.append(node_number_i)
    for node_number_i in k_high_deg_nodes_num:
        # print("node_number_i :", node_number_i)
        # circle_u = Circle(d, u)
        circle_i = Circle(net.r, net.nodes[node_number_i])
        # Insert to set_t the nodes which are in the circle of node_number_i
        for node_number_j in nodes_number_list:
            # print("nodes_number_list :", nodes_number_list)
            # print("node_number_j :", node_number_j)
            # Calculate the relation of node_number_j to the circle of node_number_i
            val = circle_i.calculate_relation_to_circle(net.nodes[node_number_j])
            if val <= 0:
                # print("val <= 0")
                # if node_number_j is already at the cut
                if node_number_j in set_s_centers:
                    # print("continue")
                    continue
                len_of_cut += 1
                # print("len_of_cut :", len_of_cut)
                if not(node_number_j in set_t):
                    # print("append and remove")
                    set_t.append(node_number_j)
                    degree_list.remove(degree_list[indexes_list.index(node_number_j)])
                    indexes_list.remove(node_number_j)
        # Update degree_list and indexes_list
        degree_list.remove(degree_list[indexes_list.index(node_number_i)])
        indexes_list.remove(node_number_i)
    if len(indexes_list) > 0:
        nodes_number_list = indexes_list
        # Call recursion
        set_s_centers, set_t, len_of_cut = divide_to_groups(net, len_of_cut, set_s_centers, set_t,
                                                            degree_list, indexes_list, nodes_number_list)
    return set_s_centers, set_t, len_of_cut


# -----------------------------------------------------------------------------------------------------

def maximal_cut_gnr_random_centers(net, set_s_centers, set_t):
    degree_list, indexes_list = cal_sort_nodes_by_degree(net)
    set_s_centers, set_t, len_of_cut = divide_to_groups(net, 0, set_s_centers, set_t, degree_list, indexes_list,
                                                        list(np.arange(len(net.nodes))))
    print("len of a :", len(set_s_centers))
    print("len of b :", len(set_t))
    print("sum of a+b :", len(set_s_centers) + len(set_t))
    print("len of cut :", len_of_cut)
    # For G(n,r) : need to divide len of edges in 2
    print("len of edges :", len(net.edges) / 2)
    print("len of cut / num of edges :", 2 * len_of_cut / len(net.edges))
    center_nodes = []
    for center_num in set_s_centers:
        center_nodes.append(net.nodes[center_num])
    net.draw_network("maximal_cut", nodes_list=center_nodes)
    set_s_points = []
    set_t_points = []
    for point_s_i in set_s_centers:
        set_s_points.append(net.nodes[point_s_i])
    for point_t_i in set_t:
        set_t_points.append(net.nodes[point_t_i])
    return set_s_points, set_t_points, len_of_cut


# -----------------------------------------------------------------------------------------------------

def main():
    n = 10
    r = 0.6
    net = generate_model(n, r)
    set_s_centers = []
    set_t = []
    set_s_centers, set_t, len_of_cut = maximal_cut_gnr_random_centers(net, set_s_centers, set_t)


if __name__ == '__main__':
    main()
