from queue import Queue
import math

__author__ = "Michael Graham - mig445 - 11139592"
__email__ = "mig445@mail.usask.ca"
# Creation date: February 7, 2016


class Problem:
    def __init__(self, initial_state, goal, graph):
        """
        Initializes a problem (who'd wanna do that?)
        :param initial_state: state is the start node
        :param goal: the goal node
        :param graph: the graph
        :return: an initialized problem
        """
        self.state = initial_state
        self.goal = goal
        self.graph = graph

    def state(self):
        """
        A state is essentially a node in the graph
        :return: the initial state
        """
        return self.state

    def goal(self):
        """
        The goal is the state that we wish to reach.
        :return: The goal state
        """
        return self.goal

    def graph(self):
        """
        The problem graph
        :return:
        """
        return self.graph

    def is_goal(self, state):
        """
        Checks if the current state is the goal
        :param state: the current node
        :return: True if the current state is the goal
        """
        return state == self.goal

    def successors(self, new_state):
        """
        Returns the successors of the current state (node)
        :param new_state: the current node of the graph
        :return: the children of the state (node)
        """
        return self.graph[new_state]


class StateQueue(Queue):
    def __init__(self, problem):
        """
        Initializes a state queue
        :param problem: a problem -- see above
        :return: an initialized state queue
        """
        super(Queue).__init__()
        self.problem = problem
        self.put(problem.state)

    def add(self, state):
        self.put(state)
        # If the search doesn't record the previously visited node it will never result in a failed search.
        # If the goal node is reached, the prev_state doesn't need to be recorded.


class TreeSearch:
    def __init__(self):
        """
        Initializes a tree search
        :return: an initialized tree search
        """

    @staticmethod
    def search(problem):
        # if queue size is 0 its size will be limitless or until I run out of memory.
        queue = StateQueue(problem)

        while not queue.empty():
            here = queue.get()

            if problem.is_goal(here):
                queue.add(here)
                return queue

            else:
                for next_s in problem.successors(here):
                    queue.add(next_s)
        return "Failed Search:"
