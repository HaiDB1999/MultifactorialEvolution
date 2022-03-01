import numpy as np

def check_cycle(parents_node):
    # """
    # :param parents_node: Các node cha (kiểu gene)
    # :return:
    #     0: Không phải chu trình
    #     1: Tồn tại chu trình
    # """
    edges = []

    # (parent, child)
    for i in range(1, len(parents_node)):
        edges.append((parents_node[i], i))

    duyet = np.zeros(len(parents_node))
    duyet[0] = 1
    queue = [0]
    while (len(queue) > 0):
        parent = queue.pop()
        childs = [x[1] for x in edges if (x[0] == parent)]

        # print(childs)
        for child in childs:
            if (duyet[child] == 0):
                duyet[child] = 1
                queue.append(child)

                # remove edge is visited
                edges.remove((parent, child))

    if (sum(duyet == 0) == 0):
        return 0
    return 1

######################################################
e_elec = 50*(10**-9)
e_fs = 10*(10**-12)
e_mp = 0.0013*(10**-12)
e_da = 5*(10**-12)
d0 = (e_fs/e_mp)**0.5
MAX_ENERRY = 10**5
do_sau = 15
######################################################
def encode(genes, config):
    n_relay = config['n_relay']
    n_sensor = config['n_sensor']

    n_relay_init = sum(genes == 0) - 1
    genes_encode = np.zeros(n_relay+1)
    for node_value in genes[genes != 0][:n_sensor]:
        node_add = node_value
        if(node_value <= n_relay_init):
            node_add = node_value % n_relay
            if(node_add == 0):
                node_add = n_relay
        else: # node sensor
            node_add = (node_value - n_relay_init) % n_sensor
            if(node_add == 0):
                node_add = n_sensor
            node_add = n_relay + node_add
        genes_encode = np.append(genes_encode, node_add)
    return genes_encode

def get_distance_to(node1, node2, list_coordinates):
    # """
    # :param node1: node1
    # :param node2: node2
    # :param list_coordinates: List tọa độ của tất cả các node
    # :return: khoảng cách euclid giữa node1 và node2
    # """
    return np.sqrt(sum((list_coordinates[int(node1)] - list_coordinates[int(node2)]) ** 2))

def E_distance(node, nodes_parent, list_coordinates, radius):
    # """
    # :param node: node
    # :param nodes_parent: Danh sách node cha (node con là các index trong danh sách)
    # :param list_coordinates: List tọa độ của tất cả các node
    # :return: Năng lượng của node
    # :radius: Bán kính truyền thông kết nối
    # """
    parent = nodes_parent[node]
    d = get_distance_to(node, parent, list_coordinates)

    # check độ sâu
    dem = 2
    while (parent != 0):
        parent = nodes_parent[int(parent)]
        dem += 1
        if (dem > do_sau):
            # print("ERROR max hop {}".format(node))
            return MAX_ENERRY

    if (dem > do_sau):
        # print("ERROR max hop {}".format(node))
        return MAX_ENERRY

    if (d <= d0):
        return (e_elec + e_fs * d * d)
    elif (d <= radius):
        return (e_elec + e_mp * (d ** 4))
    else:
        # print("Gia tri: {}".format(d))
        # return (e_elec + e_mp * (d ** 4))
        # print("ERROR E_distance {}".format(nodes_parent[node], node))
        return MAX_ENERRY

def Energy_consumption_sensor(genes, config):
    # """
    # :param indiv: Kiểu genes
    # :param config: Chứa các config của mạng
    # :return: fitness của indiv
    # """
    nodes_parent = genes
    nodes_child = np.arange(1, len(genes))
    list_coordinates = config['list_coordinates']
    radius = config['radius']

    if(check_cycle(nodes_parent)):
        return MAX_ENERRY*2*4000

    _max = 0
    for node in nodes_child:
        if (nodes_parent[node] != 0):  # relays node
            nums_childs = sum(nodes_parent == node)
            E_node = nums_childs * e_elec + (nums_childs + 1) * e_da + E_distance(node, nodes_parent, list_coordinates, radius)
            if(E_node >= MAX_ENERRY):
                return E_node*4000
        else:
            nums_childs = sum(nodes_parent == node)
            E_node = nums_childs * (e_elec + e_da) + E_distance(node, nodes_parent, list_coordinates, radius)
            if(E_node >= MAX_ENERRY):
                return E_node*4000
        _max = np.max([_max, E_node])

    return _max * 4000

def reset_rank(arr:list):
    # """
    # :param arr:
    # :return: Gia tri cua rank cua cac node
    # """
    arr_index = [(i, arr[i]) for i in range(len(arr))]
    arr_index.sort(key = lambda x: x[1])
    arr_rank = [(arr_index[i][0], i+1) for i in range(len(arr_index))]
    arr_rank.sort(key = lambda x: x[0])
    return [x[1] for x in arr_rank]


