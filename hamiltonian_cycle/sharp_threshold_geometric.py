import geometric_network as Ge_net
import point as Pnt
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# import random as rd


# -----------------------------------------------------------------------------------------------------------
# Divide the unit cube into sectors depends on the value of r

def divide_to_grid(net, n, r):
    # num_of_groups = int(np.floor((2 / r) ** 2))
    num_of_one_side = int(np.floor((2 / r)))
    arr_of_nodes = np.array(net.nodes)

    # Unable to use np.array due to different length of sub groups
    groups_on_grid = []

    # Divide the nodes to groups by their coordinates
    # Double loop, doesnt depend on the size of the input n but rather on r which is a small value
    # Does not affect the linearity of the algorithm
    i = 0
    for x in range(num_of_one_side):
        for y in range(num_of_one_side):
            arr = subgroup_by_condition(arr_of_nodes, x * (r / 2), (x + 1) * (r / 2), y * (r / 2), (y + 1) * (r / 2))
            dict_square = {'i': i, 'arr_points': arr, 'bnd_x_down': x * (r / 2), 'bnd_x_up': (x + 1) * (r / 2),
                           'bnd_y_down': y * (r / 2), 'bnd_y_up': (y + 1) * (r / 2), 'degree': len(arr),
                           'index_graph': -1, 'is_den': is_dense(arr, n, r)}
            groups_on_grid.append(dict_square)
            # groups.append(arr)
            i += 1
    # print_squares_arr(groups)
    return groups_on_grid  # list od dictionary


# -----------------------------------------------------------------------------------------------------------
# Calculate the threshold between sparse and dense

def calculate_threshold(n, r):
    num_of_groups = int(np.floor((2 / r) ** 2))
    return int(np.floor(n / (num_of_groups * 2)))


# -----------------------------------------------------------------------------------------------------------
# Return np.array after filtering the points, only points within the current sector will be inside

def subgroup_by_condition(arr_of_nodes, bnd_x_down, bnd_x_up, bnd_y_down, bnd_y_up):
    """subgrp_lst = []
        for i in range(0, len(group)):
            if group[i].x_value >= bnd_x_down and group[i].x_value < bnd_x_up and
             group[i].y_value >= bnd_y_down and group[i].y_value < bnd_y_up:subgrp_lst.append(group[i])
        return np.array(subgrp_lst)"""
    return np.array(list(filter(
        lambda p: bnd_x_down <= p.x_value < bnd_x_up and bnd_y_down <= p.y_value < bnd_y_up,
        arr_of_nodes)))


# -----------------------------------------------------------------------------------------------------------
# Get arr_nodes and check if dense

def is_dense(arr_points, n, r):
    threshold = calculate_threshold(n, r)
    if len(arr_points) > threshold:
        return True
    return False


# -----------------------------------------------------------------------------------------------------------
# Divide groups_on_grid to sparse and dense

def divide_dense_from_sparse(groups_on_grid):
    dense_group = []
    sparse_group = []
    for i in range(len(groups_on_grid)):
        if groups_on_grid[i]['is_den']:
            dense_group.append(groups_on_grid[i])
        else:
            sparse_group.append(groups_on_grid[i])
    return dense_group, sparse_group  # lists of dictionaries


# -----------------------------------------------------------------------------------------------------------
# Connect between every point in a sparse square to a dense square

def label_sparse_point_to_dense(net, groups_on_grid, dense_group, sparse_group, r):
    # To match to a square or to a point??
    # ???
    """sparse_point_list = []
    for sparse_square in sparse_group:
        for p in sparse_square:
            sparse_point_list.append(p)"""
    # for p in sparse_point_list:

    '''
    For i in range (-2, 3)#without himself
      For j in range (-2, 3)
    1)In dense squares if boundaries x = i*myboundry  and y = j*myboundry insert to my friends 
    2)For every point in me try to match a point that is connected to me (do not go through all point in it)
    '''

    # Dictionary that contains lists of dense friends of each sparse square
    friends_dict = {}
    for sparse_index, sparse_square in enumerate(sparse_group):
        # For each sparse square get his friends(at most 24)
        curr_friends = []
        for dense_square in dense_group:
            if is_friend(sparse_square, dense_square, r):
                curr_friends.append(dense_square)  # curr_friends can be empty - if the square is empty
        print("The list of friends of i =", sparse_square['i'], "is :")
        print_list_of_dict(curr_friends)
        friends_dict[str(sparse_square['i'])] = curr_friends
        print("#####################################################")
    ''' for sparse_index, sparse_square in enumerate(sparse_group):
        # For each sparse square get his friends(at most 24)
        curr_friends = []
        for dense_index, dense_square in enumerate(dense_group):
            if is_friend(sparse_square, dense_square, r) == True:
                curr_friends.append(dense_square) # curr_friends can be empty - if the square is empty
        print("The list of friends of i =", sparse_square['i'], "is :")
        print_list_of_dict(curr_friends)
        friends_dict[str(sparse_index)] = curr_friends
        print("#####################################################")'''
    # filtered_list = list(filter(lambda dense_square: is_friend(sparse_square, dense_square), dense_group))
    # print("The list of friends of i =",index, "is :" ,filtered_list)

    # Initialize data structures : dictionary by the length of the sparse group
    # For each sparse there will be a dictionary for all its vertices
    # For each vertex there will be a list containing two vertices connecting to this vertex by the greedy algorithm
    # The efficiency is linear because the length of the sparse square is very low
    # In addition, the sum of the lengths of each dictionary is the number of nodes in g_tag

    '''dict_labels = {}
    for curr_square in sparse_group:
        dict_square = {}
        serial_str_sq = str(curr_square['i'])
        for p in curr_square['arr_points']:
            serial_str_point = str(p.serial_number)
            dict_square[serial_str_point] = build_pair(net, p, friends_dict[serial_str_sq], curr_square['degree'])
        dict_labels[serial_str_sq] = dict_square


    # Run all over the sparse squares and insert an edge to g_tag between the square and its friend if they're connected
    for k in friends_dict.keys():
        num_of_sparse = int(k)
        list_of_sparse_sq = friends_dict[k]'''

    return friends_dict


# -----------------------------------------------------------------------------------------------------------
# Build g'

def build_g_tag(net, dense_group, threshold):
    """
     dict_square = {'i': i, 'arr_points': arr, 'bnd_x_down': x * (r / 2), 'bnd_x_up': (x + 1) * (r / 2),
                           'bnd_y_down': y * (r / 2), 'bnd_y_up': (y + 1) * (r / 2), 'degree': len(arr),
                           'index_graph': -1, 'is_den': is_dense(arr, n, r)}
    """
    g_tag = nx.Graph()
    # Add vertices to the g_tag
    counter = 0
    for sq in dense_group:
        if sq['degree'] != 0:
            pos_x = 0.5 * (sq['bnd_x_down'] + sq['bnd_x_up'])
            pos_y = 0.5 * (sq['bnd_y_down'] + sq['bnd_y_up'])
            g_tag.add_node(counter, pos=(pos_x, pos_y))
            sq['index_graph'] = counter
            counter += 1
            print("g_tag point number:", sq['index_graph'], "number of square:", sq['i'], "degree:", sq['degree'])

    # Run all over groups_on_grid in 2 loops
    # If they both sparse -> continue (we don't want to connect sparse square to each other)
    # Else : check if there is an edge between the two groups -> add edge between the squares to g_tag
    for sq1 in dense_group:
        for sq2 in dense_group:
            if sq1 != sq2 and g_tag.has_edge(sq2['index_graph'], sq1['index_graph']) is False and are_squares_connected(
                    net, sq1, sq2):
                # if sq1 != sq2 and are_squares_connected(net, sq1, sq2):
                # g_tag.add_edge(sq1['index_graph'], sq2['index_graph'], weight=sq1['degree']+sq2['degree'])
                # Try - random weight
                w = abs(sq1['bnd_x_up'] - sq2['bnd_x_up']) + abs(sq1['bnd_y_up'] - sq2['bnd_y_up'])
                g_tag.add_edge(sq1['index_graph'], sq2['index_graph'], weight=w)
                print("Weight of (", sq1['index_graph'], ",", sq2['index_graph'], ") is :", w)
    return g_tag


'''def build_g_tag(net, groups_on_grid, threshold):
    g_tag = nx.Graph()
    # Add vertices to the g_tag
    counter = 0
    for sq in groups_on_grid:
        if sq['degree'] != 0:
            g_tag.add_node(counter)
            sq['index_graph'] = counter
            counter += 1
            print("g_tag point number:", sq['index_graph'], "number of square:", sq['i'])
    # Run all over groups_on_grid in 2 loops
    # If they both sparse -> continue (we don't want to connect sparse square to each other)
    # Else : check if there is an edge between the two groups -> add edge between the squares to g_tag
    for sq1 in groups_on_grid:
        for sq2 in groups_on_grid:
            if sq1['degree'] <= threshold and sq2['degree'] <= threshold:
                continue
            if are_squares_connected(net, sq1, sq2):
                g_tag.add_edge(sq1['index_graph'], sq2['index_graph'])
    return g_tag'''


# -----------------------------------------------------------------------------------------------------------
# Get two squares and return point 1 in square 1 connected to point 2 in square 2

def points_connect_between_squares(net, sq1, sq2):
    for p1 in sq1['arr_points']:
        for p2 in sq2['arr_points']:
            if net.is_at_edge_by_points(net.edges, p1.serial_number, p2.serial_number):
                return p1.serial_number, p2.serial_number
    return -1, -1


# -----------------------------------------------------------------------------------------------------------
# Get two squares and return true if its connected

def are_squares_connected(net, sq1, sq2):
    for p1 in sq1['arr_points']:
        for p2 in sq2['arr_points']:
            if net.is_at_edge_by_points(net.edges, p1.serial_number, p2.serial_number):
                return True
    return False


# -----------------------------------------------------------------------------------------------------------
# Get a network, a point and list containing the friends of the square p where p is
# Return a list of flag two points assign to the current point

def build_pair(net, p, list_of_friends, curr_degree):
    in_out_list = []
    flag = 0
    for sq in list_of_friends:
        for point in sq['arr_points']:
            if net.is_at_edge_by_points(net.edges, point.serial_number, p.serial_number):
                square_point_list = []
                square_point_list.append(sq)
                sq['degree'] -= 1
                in_out_list.append(square_point_list)
                if curr_degree == 1:
                    if flag == 1:
                        return in_out_list
                    flag = 1
                    continue
                else:
                    return in_out_list
    return in_out_list


# -----------------------------------------------------------------------------------------------------------
# Get group and index and return the square of its index

def find_square_by_point(groups_on_grid, index):
    if index < 0 or index >= len(groups_on_grid):
        return np.nan
    for sq in groups_on_grid:
        if sq['index_graph'] == index:
            return sq
    return np.nan


# -----------------------------------------------------------------------------------------------------------
# Return if the squares are friends

def is_friend(sparse_square, dense_square, r):
    for i in range(-2, 3):
        for j in range(-2, 3):
            '''print("&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%&%")
            print("dense_square['bnd_x_down'] :", dense_square['bnd_x_down'])
            print("sparse_square['bnd_x_down'] + i*(r/2) :", sparse_square['bnd_x_down'] + i*(r/2))
            print("dense_square['bnd_x_up'] :", dense_square['bnd_x_up'])
            print("sparse_square['bnd_x_up'] + i*(r/2) :", sparse_square['bnd_x_up'] + i*(r/2))
            print("dense_square['bnd_y_down'] :", dense_square['bnd_y_down'])
            print("sparse_square['bnd_y_down'] + i*(r/2) :", sparse_square['bnd_y_down'] + i*(r/2))
            print("dense_square['bnd_y_up'] :", dense_square['bnd_y_up'])
            print("sparse_square['bnd_y_up'] + i*(r/2) :", sparse_square['bnd_y_up'] + i*(r/2))'''
            if dense_square['bnd_x_down'] == sparse_square['bnd_x_down'] + i * (r / 2) and dense_square['bnd_x_up'] == \
                    sparse_square['bnd_x_up'] + i * (r / 2):
                if dense_square['bnd_y_down'] == sparse_square['bnd_y_down'] + j * (r / 2) and \
                        dense_square['bnd_y_up'] == sparse_square['bnd_y_up'] + j * (r / 2):
                    return True
    return False


# -----------------------------------------------------------------------------------------------------------
# Build g_two_tags

def add_sparses_to_dense_tree(g_two_tags, net, groups_on_grid, friends_dict):
    # Run over the dense friend of the sparse squares and add to g_two_tags edge between connected squares
    counter = len(g_two_tags.nodes)
    for k in friends_dict.keys():
        num_of_sparse = int(k)
        print("k:", k, "num_of_sparse:", num_of_sparse)
        curr_sparse = groups_on_grid[num_of_sparse]
        if curr_sparse['degree'] == 0:
            continue
        # Add node that represents this square
        pos_x = 0.5 * (curr_sparse['bnd_x_down'] + curr_sparse['bnd_x_up'])
        pos_y = 0.5 * (curr_sparse['bnd_y_down'] + curr_sparse['bnd_y_up'])
        g_two_tags.add_node(counter, pos=(pos_x, pos_y))
        curr_sparse['index_graph'] = counter
        list_of_friends = friends_dict[k]
        print("g_two_tags point number:", curr_sparse['index_graph'], "number of square:", curr_sparse['i'], "degree:",
              curr_sparse['degree'])
        # Add edge that represents connection between the current sparse and one of its dense friend
        for dense_sq in list_of_friends:
            if are_squares_connected(net, curr_sparse, dense_sq):
                '''g_two_tags.add_edge(curr_sparse['index_graph'], dense_sq['index_graph'],
                                    weight=curr_sparse['degree'] + dense_sq['degree'])
                print("Weight of (", curr_sparse['index_graph'], ",", dense_sq['index_graph'], ") is :",
                      curr_sparse['degree'] + dense_sq['degree'])'''
                w = abs(curr_sparse['bnd_x_up'] - dense_sq['bnd_x_up']) + abs(curr_sparse['bnd_y_up'] - dense_sq['bnd_y_up'])
                g_two_tags.add_edge(curr_sparse['index_graph'], dense_sq['index_graph'], weight=w)
                print("Weight of (", curr_sparse['index_graph'], ",", dense_sq['index_graph'], ") is :", w)
                break
        counter += 1
    return g_two_tags


# -----------------------------------------------------------------------------------------------------------
# Get g_two_tags and add in time and out time for each square

def add_in_out_times(g_two_tags):
    # Initialization
    all_in_out_times = []
    for sq in g_two_tags.nodes:
        all_in_out_times.append([])
    return add_times_dfs(g_two_tags, (list(g_two_tags.nodes))[0], all_in_out_times)


# -----------------------------------------------------------------------------------------------------------
# The Run over g'' by dfs and add in out time
def add_times_dfs(g_two_tags, start, all_in_out_times):
    visited = set()
    counter, all_in_out_times = add_times_dfs_utility(g_two_tags, start, visited, all_in_out_times, 0)
    return counter, all_in_out_times


def add_times_dfs_utility(g_two_tags, start, visited, all_in_out_times, counter):
    visited.add(start)
    print(start, end=' ')
    all_in_out_times[start].append(counter)
    counter += 1
    for neighbour in g_two_tags.neighbors(start):
        if neighbour not in visited:
            counter, all_in_out_times = add_times_dfs_utility(g_two_tags, neighbour, visited, all_in_out_times, counter)
            print(start, end=' ')
            all_in_out_times[start].append(counter)
            counter += 1
    '''if len(g_two_tags.neighbors(start)) != 0:
        all_in_out_times[start].append(counter)'''
    return counter, all_in_out_times


# -----------------------------------------------------------------------------------------------------------
# Travel across g_two_tags by in-out times and build cycle

def travel_squares_by_times_and_build_cycle(net, g_two_tags, groups_on_grid, counter, all_in_out_times):
    temp_sq_num_of_first = -1
    path = []
    path_points_obj = []
    for i in range(counter + 1):
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("iteration i =", i)
        index_point_i, curr_sq_i = square_of_counter(groups_on_grid, i, all_in_out_times)
        print("curr_sq_i['index_graph'] :", curr_sq_i['index_graph'])
        if i == 0:
            temp_sq_num_of_first = curr_sq_i['index_graph']
            path.append(curr_sq_i['arr_points'][i].serial_number)
            path_points_obj.append(curr_sq_i['arr_points'][i])
            # print("path:", path)
            curr_sq_i['arr_points'] = np.delete(curr_sq_i['arr_points'],
                                                np.where(curr_sq_i['arr_points'] == curr_sq_i['arr_points'][i]))
        # **************************************************************************************************
        # If there is not a cycle

        if i + 1 == counter and index_point_i != temp_sq_num_of_first:
            print("Algorithm failed to find hamilton cycle :(")
            return
        # **************************************************************************************************

        if i + 1 == counter and index_point_i == temp_sq_num_of_first:
            for j in range(len(curr_sq_i['arr_points'])):
                path.append(curr_sq_i['arr_points'][0].serial_number)
                path_points_obj.append(curr_sq_i['arr_points'][0])
                # print("path:", path)
                curr_sq_i['arr_points'] = np.delete(curr_sq_i['arr_points'],
                                                    np.where(curr_sq_i['arr_points'] == curr_sq_i['arr_points'][0]))
            break
        index_i_plus_one, curr_sq_i_plus_one = square_of_counter(groups_on_grid, i + 1, all_in_out_times)
        print("curr_sq_i_plus_one['index_graph'] :", curr_sq_i_plus_one['index_graph'])

        # **************************************************************************************************
        # If curr_sq_i is sparse or If curr_sq_i is dense and this is the last time we visit this square

        # if (not curr_sq_i['is_den']) or (curr_sq_i['is_den'] is True and len(all_in_out_times[index_point_i]) == 1):
        if (not curr_sq_i['is_den']) or (curr_sq_i['is_den'] is True and all_in_out_times[index_point_i][len(all_in_out_times[index_point_i])-1] == i):
            print("last time condition")
            temp_exit_point, temp_next_point = get_exit_point_last_visit(net, path_points_obj[len(path_points_obj) - 1],
                                                                         curr_sq_i, curr_sq_i_plus_one)
            if temp_exit_point is None or temp_next_point is None:
                print("Algorithm failed to find hamilton cycle :(")
                return path
            else:
                print("temp_exit_point :", temp_exit_point.serial_number)
                print("temp_next_point :", temp_next_point.serial_number)
            # Add to cycle all points in this square
            for j in range(len(curr_sq_i['arr_points'])):
                if temp_exit_point.serial_number != curr_sq_i['arr_points'][0].serial_number:
                    path.append(curr_sq_i['arr_points'][0].serial_number)
                    path_points_obj.append(curr_sq_i['arr_points'][0])
                    # print("path:", path)
                curr_sq_i['arr_points'] = np.delete(curr_sq_i['arr_points'],
                                                    np.where(curr_sq_i['arr_points'] == curr_sq_i['arr_points'][0]))
            if temp_exit_point.serial_number != path_points_obj[len(path_points_obj) - 1].serial_number:
                path.append(temp_exit_point.serial_number)
                path_points_obj.append(temp_exit_point)
                curr_sq_i['arr_points'] = np.delete(curr_sq_i['arr_points'],
                                                    np.where(curr_sq_i['arr_points'] == temp_exit_point))
                # print("path:", path)
            # curr_sq_i_plus_one,next_point, flag=get_first_point_connected(net,path[len(path)-1],curr_sq_i_plus_one)

            path.append(temp_next_point.serial_number)
            path_points_obj.append(temp_next_point)
            # print("path:", path)
            curr_sq_i_plus_one['arr_points'] = np.delete(curr_sq_i_plus_one['arr_points'],
                                                         np.where(curr_sq_i_plus_one['arr_points'] == temp_next_point))

        # **************************************************************************************************
        # If curr_sq_i is dense and this is not the last time we visit this square

        # if curr_sq_i['is_den'] and len(all_in_out_times[index_point_i]) > 1:
        if curr_sq_i['is_den'] and all_in_out_times[len(all_in_out_times) - 1] != i:
            print("not last time condition")
            temp_exit_point, temp_next_point = get_exit_point_not_last_visit(net,
                                path_points_obj[len(path_points_obj) - 1], curr_sq_i, curr_sq_i_plus_one)
            if temp_exit_point is None or temp_next_point is None:
                print("Algorithm failed to find hamilton cycle :(")
                return path
            print("temp_exit_point :", temp_exit_point.serial_number)
            print("temp_next_point :", temp_next_point.serial_number)
            if temp_exit_point.serial_number != path_points_obj[len(path_points_obj) - 1].serial_number:
                path.append(temp_exit_point.serial_number)
                path_points_obj.append(temp_exit_point)
                curr_sq_i['arr_points'] = np.delete(curr_sq_i['arr_points'],
                                                    np.where(curr_sq_i['arr_points'] == temp_exit_point))
                # print("path:", path)
            # If there is edge to the next square
            path.append(temp_next_point.serial_number)
            path_points_obj.append(temp_next_point)
            # print("path:", path)
            curr_sq_i_plus_one['arr_points'] = np.delete(curr_sq_i_plus_one['arr_points'],
                                                         np.where(curr_sq_i_plus_one['arr_points'] == temp_next_point))
        print("path :", path)
    return path


# -----------------------------------------------------------------------------------------------------------
# Get network, point and square, return point in this square that is connected to the given point and the update square
# In case that this is last time we visit in this square

def get_exit_point_last_visit(net, curr_point_obj, curr_sq, next_sq):
    # if the current point is the exit point
    if len(curr_sq['arr_points']) == 0:
        for next_point in next_sq['arr_points']:
            if net.is_at_edge_by_points(net.edges, curr_point_obj.serial_number, next_point.serial_number):
                return curr_point_obj, next_point
        return None, None
    # Search for point connected to next square
    for temp_point_i in curr_sq['arr_points']:
        for next_point_j in next_sq['arr_points']:
            if net.is_at_edge_by_points(net.edges, temp_point_i.serial_number, next_point_j.serial_number):
                return temp_point_i, next_point_j
    return None, None


# -----------------------------------------------------------------------------------------------------------
# Get network, point and square, return point in this square that is connected to the given point and the update square
# In case that this is not last time we visit in this square

def get_exit_point_not_last_visit(net, curr_point_obj, curr_sq, next_sq):
    # if the current point is the exit point
    for next_point in next_sq['arr_points']:
        if net.is_at_edge_by_points(net.edges, curr_point_obj.serial_number, next_point.serial_number):
            return curr_point_obj, next_point
    # Search for point connected to next square
    for temp_point_i in curr_sq['arr_points']:
        for next_point_j in next_sq['arr_points']:
            if net.is_at_edge_by_points(net.edges, temp_point_i.serial_number, next_point_j.serial_number):
                return temp_point_i, next_point_j
    return None, None


# -----------------------------------------------------------------------------------------------------------
# Get network, point and square
# return first point in this square that is connected to the given point and the update square

def get_first_point_connected(net, curr_point_serial_number, next_sq):
    for next_point in next_sq['arr_points']:
        if net.is_at_edge_by_points(net.edges, curr_point_serial_number, next_point.serial_number):
            '''# Delete from arr_point so we wont pass again in this point
            np.delete(next_sq['arr_points'], np.where(next_sq['arr_points'] == next_point))'''
            return next_sq, next_point, 0
    return next_sq, np.nan, 1


# -----------------------------------------------------------------------------------------------------------
# Return the matching point number of the point in g'' that have this counter in time-list
# In addition the function return the relevant square represented by the point

def square_of_counter(groups_on_grid, counter, all_in_out_times):
    print("counter :", counter)
    # Get the point that has the current time (counter) in all_in_out_times
    point_number = 0
    for i, lst in enumerate(all_in_out_times):
        for j in range(len(lst)):
            if lst[j] == counter:
                point_number = i
    # Get the square of index
    for sq in groups_on_grid:
        if sq['index_graph'] == point_number:
            return point_number, sq
    return np.nan, np.nan


# -----------------------------------------------------------------------------------------------------------

def rec_dfs(net, parent, child):
    if len(list(net.neighbors(child))) == 1:
        print(child, ","),
    else:
        print(parent)
        for v in net.neighbors(child):
            if parent != v:
                rec_dfs(net, child, v)
                print(child)


# -----------------------------------------------------------------------------------------------------------
# Print functions

def print_squares_arr(squares_arr):
    for i, sq in enumerate(squares_arr):
        print("square number : i =", i)
        print_point_arr(sq)


def print_list_of_dict(list_of_dict):
    for i in range(len(list_of_dict)):
        print("i =", list_of_dict[i]['i'], ",boundaries of x:", list_of_dict[i]['bnd_x_down'], ",",
              list_of_dict[i]['bnd_x_up'], "boundaries of y:", list_of_dict[i]['bnd_y_down'],
              ",", list_of_dict[i]['bnd_y_up'])
        print_point_arr(list_of_dict[i]['arr_points'])


def print_point_arr(point_arr):
    for i in range(0, len(point_arr)):
        point_arr[i].print_point()


# -----------------------------------------------------------------------------------------------------------
# main

def main():
    r = 0.5
    n = 200
    net = Ge_net.Network(r)
    for i in range(0, n):
        p = Pnt.Point(i)
        net.add_vertex(p)
    net.make_edges()
    net.draw_network()
    print("Edges :")
    net.print_edge_arr(net.edges)
    groups_on_grid = divide_to_grid(net, n, r)
    print("========================================================================================")
    print("groups_on_grid:")
    print_list_of_dict(groups_on_grid)
    # Make sure num_of_squares is squared!!!!!!!!!!!!!!!!!!
    threshold = calculate_threshold(n, r)
    print("========================================================================================")
    print("threshold:", threshold)
    # dense_group, sparse_group = divide_dense_from_sparse(groups_on_grid, n, r)
    dense_group, sparse_group = divide_dense_from_sparse(groups_on_grid)
    print("========================================================================================")
    print("Dense group:")
    print_list_of_dict(dense_group)
    print("len of dense group:", len(dense_group))
    print("========================================================================================")
    print("Sparse group:")
    print_list_of_dict(sparse_group)
    print("len of sparse group:", len(sparse_group))
    print("========================================================================================")
    print("g_tag:")
    g_tag = build_g_tag(net, dense_group, threshold)
    pos_g_tag = nx.get_node_attributes(g_tag, 'pos')
    nx.draw(g_tag, pos_g_tag, with_labels=True)
    labels_g_tag = nx.get_edge_attributes(g_tag, 'weight')
    nx.draw_networkx_edge_labels(g_tag, pos_g_tag, label_pos=0.3, edge_labels=labels_g_tag)
    plt.savefig("g_tag_drawing.png")
    plt.show()
    print("========================================================================================")
    print("spanning tree of g_tag:")
    # Build spanning tree of g_tag
    # g_tag_spanning_tree = nx.maximum_spanning_tree(g_tag)
    g_tag_spanning_tree = nx.minimum_spanning_tree(g_tag)
    # nx.draw(g_tag_spanning_tree, with_labels=True)
    # plt.savefig("g_tag_spanning_tree_drawing.png")
    # plt.show()
    for ele in list(g_tag_spanning_tree.edges(data='weight')):
        print("Weight of (", ele[0], ",", ele[1], ") is :", ele[2])
    pos_g_tag_spanning_tree = nx.get_node_attributes(g_tag_spanning_tree, 'pos')
    nx.draw(g_tag_spanning_tree, pos_g_tag_spanning_tree, with_labels=True)
    labels_g_tag_spanning_tree = nx.get_edge_attributes(g_tag_spanning_tree, 'weight')
    nx.draw_networkx_edge_labels(g_tag_spanning_tree, pos_g_tag_spanning_tree, label_pos=0.3,
                                 edge_labels=labels_g_tag_spanning_tree)
    plt.savefig("g_tag_spanning_tree_drawing.png")
    plt.show()
    print("========================================================================================")
    g_two_tags = g_tag_spanning_tree.copy()
    print("friend_dict of sparse squares in g_two_tags:")
    friends_dict = label_sparse_point_to_dense(net, groups_on_grid, dense_group, sparse_group, r)
    print("========================================================================================")
    print("g_two_tags:")
    g_two_tags = add_sparses_to_dense_tree(g_two_tags, net, groups_on_grid, friends_dict)
    pos_g_two_tags = nx.get_node_attributes(g_two_tags, 'pos')
    nx.draw(g_two_tags, pos_g_two_tags, with_labels=True)
    labels_g_two_tags = nx.get_edge_attributes(g_two_tags, 'weight')
    nx.draw_networkx_edge_labels(g_two_tags, pos_g_two_tags, label_pos=0.3, edge_labels=labels_g_two_tags)
    plt.savefig("g_two_tags_drawing.png")
    plt.show()
    print("========================================================================================")
    print("Dfs and adding in-out times:")
    counter, all_in_out_times = add_in_out_times(g_two_tags)
    print("\nall_in_out_times:")
    for index in range(len(all_in_out_times)):
        print("index =", index, ", all_in_out_times[index] :", all_in_out_times[index])
    # print("counter:", counter)
    print("========================================================================================")
    print("Traveling by times and build cycle:")
    path = travel_squares_by_times_and_build_cycle(net, g_two_tags, groups_on_grid, counter, all_in_out_times)
    print("Len of path :", len(path))
    print("Len of net.nodes :", len(net.nodes))
    print("path :", path)
    if len(path) == len(net.nodes):
        print("Algorithm found a cycle :)")
    # Check if number doesnt appear twice in the path
    for i_1 in range(len(path)):
        for i_2 in range(len(path)):
            if i_1 == i_2:
                continue
            if path[i_1] == path[i_2]:
                print("number appears twice")
                break

    '''
    arr = np.array([1, 2, 3])
    arr2 = np.delete(arr, 0)
    print(arr2)
    n = 20
    r = 0.4
    g = geometricModelGeneration.gen_graph(n, r)
    print(g.nodes)
    # print(g.nodes[0])
    # print(g.neighbors(g.nodes[0]))
    # print(g.neighbors(0))
    # print(len(list(g.predecessors(0))), len(list(g.successors(0))))
    print([n for n in g.neighbors(0)])
    print(type(g.neighbors(0)))
    print(list(g.neighbors(0))[0])
    # print(list(g.neighbors(0).keys())[0])
    rec_dfs(g, 0, list(g.neighbors(0))[0])
    '''


if __name__ == '__main__':
    main()

'''groups = np.empty(shape=num_of_groups, dtype=np.ndarray)
    print(type(groups))
    arr = subgroup_by_condition(arr_of_nodes, 0, 0.25, 0, 0.25)
    groups = np.array([arr])
    print("arr:")
    print_point_arr(arr)
    groups = np.vstack((groups, arr))
    print("groups:")
    print_squares_arr(groups)
    arr1 = subgroup_by_condition(arr_of_nodes, 0.25, 0.5, 0.25, 0.5)
    print("arr1:")
    print_point_arr(arr1)
    groups = np.vstack((groups, arr1))
    print("groups:")
    print_squares_arr(groups)
    arr_of_nodes = np.array(net.nodes)
    print_point_arr(arr_of_nodes)
    temp = arr_of_nodes[(arr_of_nodes, )]
    groups = np.array(temp)
    groups = np.empty(num_of_groups)
    #groups[:] = np.nan
    p0 = pnt.Point(0)
    p1 = pnt.Point(1)
    arr1 = np.array([p0, p1])
    p2 = pnt.Point(2)
    p3 = pnt.Point(3)
    arr2 = np.array([p2, p3])
    arr = np.array([arr1])
    arr = np.vstack((arr, arr2))
    print_squares_arr(arr)'''
