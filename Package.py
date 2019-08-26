from AStar import Problem, AStar


class Package:
    """
    The Package class is used to represent a package.
    \- It contains a current location for the package, a source and a destination
    """

    def __init__(self, source, destination, ID, graph):
        """
        Initializes a package
        :param source:
        :param destination:
        """
        self.ID = ID
        self.source = source
        self.destination = destination
        self.location = source
        self.path = None
        self.path_cost = 0
        self.time_spent_on_search = 0
        self.get_path_to(self.destination, graph)


    def get_path_to(self, destination, graph):
        """
        Gets a path to the specified destination if it exists
        :param destination:
        :return: The time that it took to perform that search
        """
        search_time = 0

        problem = Problem(self.location, destination, graph)

        search = AStar.search(problem)
        search_successful = search[0]
        search_time += search[3]
        if search_successful:
            self.path = search[1]
            self.path_cost = search[2]
        else:
            print("ERROR: Search could not find a path")
        # print "Path of package s->d: " + str(self.path)
        self.time_spent_on_search += search_time
