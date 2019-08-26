import heapq
import time
from Map import *

__author__ = "Michael Graham - mig445 - 11139592"
__email__ = "mig445@mail.usask.ca"
# Creation date: February 7, 2016


class Problem:
    def __init__(self, initial_state, goal_state, graph):
        """
        Initializes a problem (who'd wanna do that?)
        :param initial_state: state is the start node
        :param goal_state: the goal node
        :param graph: the graph
        :return: an initialized problem
        """
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.graph = graph

    def initial_state(self):
        """
        A state is essentially a node in the graph
        :return: the initial state
        """
        return self.initial_state

    def goal_state(self):
        """
        The goal is the state that we wish to reach.
        :return: The goal state
        """
        return self.goal_state

    def graph(self):
        """
        The problem graph
        :return: the graph of the problem
        """
        return self.graph

    def is_goal(self, state):
        """
        Checks if the current state is the goal
        :param state: the current node
        :return: True if the current state is the goal
        """
        return state == self.goal_state

    def successors(self, state):
        """
        Returns the successors of the current state (node)
        :param state: the current node of the graph
        :return: the children of the state (node)
        """
        return self.graph[state]


class StateQueue(object):
    def __init__(self, problem):
        """
        Initializes a state queue
        :param problem: a problem -- see above
        :return: an initialized state queue
        """
        super(StateQueue, self).__init__()
        self.problem = problem
        self.frontier = []
        heapq.heappush(self.frontier, (0, problem.initial_state))
        self.path = {problem.initial_state: None}  # where explored is a dictionary to keep track of visited
        self.cost = {problem.initial_state: 0}  # where cost is the cost to get to the current state

    def add(self, cost, state, parent):
        """
        Adds a state to the frontier of possible paths
          -- Frontier is a heapq (priority queue) that contains a tuple with the cost and state
        Also maintains a path of what state we came from to get to the next state
        :param cost: The cost to get to that state
        :param state: The current state
        :param parent: The parent of the state that we're at
        :return: Nothing
        """
        heapq.heappush(self.frontier, (cost, state))
        self.path[state] = parent
        self.cost[state] = cost

    def get(self):
        """
        Gets the top item from the priority queue (frontier) and returns it.
        :return: The top item of the priority queue
        """
        return heapq.heappop(self.frontier)[1]

    def empty(self):
        """
        Checks to see if the priority queue (frontier) is empty.
        :return: True if empty; otherwise False.
        """
        return not self.frontier


class AStar:
    def __init__(self):
        """
        Initializes a tree search
        :return: an initialized tree search
        """

    @staticmethod
    def search(problem):
        """
        Performs A* Search. This search is based upon the searches from the text
        Note: Based off of depth uniform search from text.

        :param problem: An initialized object of type Problem
        :return: Quadruple:
                    bool:             - A boolean value - true if search reached goal successfully, false if not
                    path:             - The path to the goal - returns None if search failed
                                            -NOTE: The path is rebuilt inside of this search (into the correct order)
                    cost:             - The cost to get to the goal - returns None if search failed
                    runtime:          - Total time that the function ran for
        """
        start_time = time.clock()                   # Time that the function started at
        if problem.initial_state in problem.graph:  # Ensures that initial state is valid
            queue = StateQueue(problem)

            while not queue.empty():
                current_state = queue.get()

                # GOAL:
                if problem.is_goal(current_state):
                    # making things more readable
                    cost = queue.cost[current_state]
                    runtime = time.clock() - start_time
                    path = AStar.make_path(queue.path, problem)

                    return True, path, cost, runtime

                else:
                    for next_state in problem.successors(current_state):

                        # HEURISTIC:
                        next_state_cost = problem.graph.get_edge_data(current_state, next_state)['weight']
                        cost = queue.cost[current_state] + next_state_cost

                        # if next_state hasn't been explored or costs less that the previous cost
                        if next_state not in queue.path or cost < queue.cost[next_state]:
                            queue.add(cost, next_state, current_state)

        runtime = time.clock() - start_time
        return False, None, None, runtime

    @staticmethod
    def make_path(path_dictionary, problem):
        """
        Rebuilds the path that search returns so that it is the correct order (from initial_state to goal_state)

        :param problem:               Object of type Problem - The original problem
        :param path_dictionary:       The path that A* recorded
        :return:                      A path that is in the correct order
        """
        current_state = problem.goal_state
        path = [current_state]                              # Set the start of the path to be that of the goal state
        while current_state != problem.initial_state:
            current_state = path_dictionary[current_state]  # Get parent from dictionary
            path.append(current_state)                      # Append the parent to the path list
        path.reverse()                                      # Reverse the list correcting the order
        return path


def test_astar():
    # CREATE GRAPH:
    # Warning: Takes around eight seconds to create graph @ size 500.
    # Warning: Will run out of memory @ around ~2000 dimension
    make_graph_time = time.clock()
    graph = makeMap(50, 50, .45)
    make_graph_time = time.clock() - make_graph_time

    # Testing A Star
    # STATES:
    initial_state = rand.choice(graph.nodes())
    goal_state = rand.choice(graph.nodes())

    # SEARCH:
    problem = Problem(initial_state, goal_state, graph)
    search_path = AStar.search(problem)

    # STATS:
    if search_path[0]:      # Search successful
        print(("Total time to create graph: " + str(make_graph_time)))
        print(("Total time to perform search: " + str(search_path[3])))
        print(("Total cost of path:" + str(search_path[2])))
        # draw_path(problem, search_path[1])
        # draw_paths(graph)

    else:                   # Search failed
        print("Search Failed!")
        print(("Total time to create graph: " + str(make_graph_time)))
        print(("Total time spent performing search:" + str(search_path[3])))

# test_astar()


