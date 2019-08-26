import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy
import random as rand


def makeMap(m, n, gapfreq):
    """ Creates a graph in the form of a grid, with mXn nodes.
    The graph has irregular holes poked into it by random deletion.

    :param m: number of nodes on one dimension of the grid
    :param n: number of nodes on the other dimension
    :param gapfreq: the fraction of nodes to delete (see function prune() below)
    :return: a networkx graph with nodes and edges.

    The default edge weight is  (see below).  The edge weights can be changed by
    designing a list that tells the frequency of weights desired.
      100% edge weights 1:  [(1,100)]
      50% weight 1; 50% weight 2: [(1,50),(2,100)]
      33% each of 1,2,5: [(1,33),(2,67),(5,100)]
      a fancy distribution:  [(1,10),(4,50),(6,90),(10,100)]
      (10% @ 1, 40% @ 4, 40% @ 6, 10% @ 10)
    """
    g = nx.grid_2d_graph(m, n)
    weights = [(1, 100)]
    prune(g, gapfreq)
    setWeights(g, weights)
    return g


def setWeights(g, weights):
    """ Use the weights list to set weights of graph g
    :param g: a networkx graph
    :param weights: a list of pairs [(w,cf) ... ]
    :return: nothing

    weights are [(w,cf) ... ]
    w is the weight, cf is the cumulative frequency

    This function uses a uniform random number to index into the weights list.
    """
    for (i, j) in nx.edges(g):
        c = rand.randint(1, 100)
        w = [a for (a, b) in weights if b >= c]  # drop all pairs whose cf is < c
        g.edge[i][j]['weight'] = w[0]  # take the first weight in w
    return


def draw(g):
    """ Draw the graph, just for visualization.  Also creates a jpg in $CWD
    :param g: a networkx graph
    :return:
    """
    pos = {n: n for n in nx.nodes(g)}
    nx.draw_networkx_nodes(g, pos, node_size=20)
    edges = nx.edges(g)
    nx.draw_networkx_edges(g, pos, edgelist=edges, width=1)
    plt.axis('off')
    plt.savefig("simplegrid.png")  # save as png
    plt.show()  # display
    return


def prune(g, gapf):
    """ Poke random holes the graph g by deleting random nodes, with probability gapf.
    Then clean up by deleting all but the largest connected component.

    Interesting range (roughly):  0.1 < gapf < 0.3
    values too far above 0.3 lead to lots of pruning, but rather smaller graphs

    :param g: a networkx graph
    :param gapf: a fraction in [0,1]
    :return: nothing
    """
    # creating gaps...
    for node in nx.nodes(g):
        if rand.random() < gapf:
            g.remove_node(node)
    # deleting all but the largest connected component...
    comps = sorted(nx.connected_components(g), key=len, reverse=False)
    while len(comps) > 1:
        nodes = comps[0]
        for node in nodes:
            g.remove_node(node)
        comps.pop(0)


def draw_path(problem, path):
    """
    Draw the graph and the path from initial_state to goal_state, just for visualization.
    -- Creates a jpg in $CWD
    -- Will be able to map multiple goal_src's hopefully.

    :param problem:               An object of type Problem.
    :param path:            The path that AStar's search returns
    :return:                Nothing
    """
    g = nx.grid_2d_graph(0, 0)

    # Get edges and nodes
    prev = None
    for item in path:
        g.add_node(item)
        if prev is not None:
            g.add_edge(item, prev)
        prev = item

    path_nodes = {node: node for node in path}
    all_nodes = {node: node for node in problem.graph}
    all_edges = problem.graph.edges()
    path_edges = g.edges()

    # labels
    labels = {problem.initial_state: 'Src', problem.goal_state: 'Dst'}

    # nodes
    nx.draw(g, all_nodes, nodelist=all_nodes, node_size=20, node_color='b')
    nx.draw(g, all_nodes, nodelist=path_nodes, node_size=40, node_color='k', labels=labels, with_labels=True)

    # edges
    nx.draw_networkx_edges(g, all_nodes, edgelist=all_edges, width=1)
    nx.draw_networkx_edges(g, all_nodes, edgelist=path_edges, width=2, edge_color='k', style='dotted')

    plt.axis('off')
    plt.savefig("simplegrid.png")
    plt.show()
    return




def draw_paths(graph, garages, trucks, p, p_being_picked_up, p_being_delivered, i):
    """
    Draw the graph and the path from initial_state to goal_state, just for visualization.
    -- Creates a jpg in $CWD
    -- Will be able to map multiple goal_src's hopefully. {node: node for node in graph}
    """

    all_nodes = {node: node for node in graph}
    all_edges = graph.edges()

    """ USED FOR DEBUGGING
    node_labels = {}
    for node in all_nodes:
        node_labels[node] = str(node)
    """

    # Create all labels
    garage_labels = {}
    truck_labels = {}
    package_labels = {}

    truck_paths = []

    truck_locations = []
    package_locations = []

    garage_locations = []

    for garage in garages:
        garage_labels[garage.location] = 'Garage'
        garage_locations.append(garage.location)

    for truck in trucks:
        truck_locations.append(truck.location)
        truck_labels[truck.location] = 'T' + str(truck.ID)
        prev = truck.location
        for item in truck.path:
            truck_paths.append((prev, item))
            prev = item

    for package in p:
        package_locations.append(package.source)
        package_locations.append(package.destination)
        package_labels[package.source] = 'P' + str(package.ID) + 'S'
        package_labels[package.destination] = 'P' + str(package.ID) + 'D'

    for package in p_being_picked_up:
        package_locations.append(package.source)
        package_locations.append(package.destination)
        package_labels[package.source] = 'P' + str(package.ID) + 'S'
        package_labels[package.destination] = 'P' + str(package.ID) + 'D'

    for package in p_being_delivered:
        package_locations.append(package.destination)
        package_labels[package.destination] = 'P' + str(package.ID) + 'D'


    # Static nodes
    nx.draw(graph, all_nodes, nodelist=all_nodes, node_size=300, node_color='b', font_size=24)
    nx.draw(graph, all_nodes, nodelist=garage_locations, node_size=500, node_color='k', labels=garage_labels, with_labels=True, font_size=24)
    nx.draw(graph, all_nodes, nodelist=package_locations, node_size=500, node_color='r', labels=package_labels, with_labels=True, font_size=24)
    # TRUCK LABELS
    # nx.draw(graph, all_nodes, nodelist=truck_locations, node_size=500, node_color='y', labels=truck_labels, with_labels=True, font_size=24)
    nx.draw(graph, all_nodes, nodelist=truck_locations, node_size=500, node_color='y', font_size=24)

    # Static edges
    nx.draw_networkx_edges(graph, all_nodes, edgelist=all_edges, width=2)
    nx.draw_networkx_edges(graph, all_nodes, edgelist=truck_paths, width = 6, style='dashed')

    fig = plt.gcf()
    fig.set_size_inches(30, 30)
    plt.axis()
    filename="Simulation\sim" + str(i) + ".png"
    plt.savefig(filename, dpi=50)
    # plt.show()
    plt.clf()       # CLEARS THE OLD GRAPH THAT WAS DRAWN
    return
