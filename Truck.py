import giffify
from Garage import *
from Package import *
from AStar import *
from String_Formatting import *
import Map

__author__ = 'Mike Graham'
__email__ = "michael.graham@usask.ca"
# February 2, 2016

map_width = 75
map_height = 33
map_noise = .4
number_of_packages = 24
number_of_trucks = 7
number_of_garages = 4
range_of_truck = 100
draw_simulation = True
make_gif = True

start_of_scenario = time.clock()
timing_list = [0]


class Truck:
    """
    The Truck class is used to represent a truck.
    It contains a current location of the truck, its home garage, and the path that it is to take next
    """

    def __init__(self, garage, max_distance, ID):
        """
        Creates a new truck
        :param garage: The truck's home garage
        """
        assert isinstance(ID, int)
        self.ID = ID
        self.garage = garage
        self.location = garage.location
        self.max_distance = max_distance
        self.package = None
        self.next_package = None
        self.path = list()
        self.path_cost = float("inf")

        # Tracking
        self.distance_traveled = 0
        self.packages_delivered = 0

    def empty(self):
        """
        Returns the current state of the truck
        :return: True if the truck is empty, false otherwise
        """
        return self.package is None

    def at_garage(self):
        """
        Tells if the truck is currently at the garage or not
        :return: True if the truck is at the garage, False otherwise
        """
        return self.location == self.garage.location

    def reset_truck(self):
        """
        Resets all of the parameters of the truck except for statistical things
        :return:
        """
        self.package = None
        self.next_package = None
        self.path = list()
        self.path_cost = float("inf")

    def next_package_unknown(self):
        """
        Determines if the truck knows what the next package is
        :return: True if the next package is not set
        """
        return self.next_package is None

    def idle(self):
        """
        Determines if the truck is currently idle
        :return: True if the truck is idle, false otherwise
        """
        return self.empty() and self.next_package_unknown()

    def destination_reached(self):
        """
        Gives the state of the truck
        :return: True if the truck has reached its current destination, False otherwise
        """
        return len(self.path) <= 0

    def can_pickup_package(self):
        """
        Lets the truck know if it can pick up the next package
        :return: True if it can pick up the package in question
        """
        return self.next_package is not None and self.location == self.next_package.location

    def pickup_package(self):
        self.package = self.next_package
        self.next_package = None

        self.path = self.package.path
        self.path_cost = self.package.path_cost
        packages_in_transit.append(self.package)
        packages_being_picked_up.remove(self.package)

    def can_drop_off_package(self):
        """
        Lets the truck know if it can drop off the next package
        :return: True if it can drop off the package in question
        """
        return self.package is not None and self.package.destination == self.location

    def drop_off_package(self):
        """
        Drops off the package
        :return:
        """
        packages_in_transit.remove(self.package)
        delivered_packages.append(self.package)
        self.reset_truck()

    def print_status(self, status):
        """
        Prints the status of the truck to the console
        :param status: The current status of the truck
        :return: N/A
        """
        sep = "--------------------------------------------------------\n"
        dvr = "  |  "
        truck = "Truck: " + str(self.ID)
        loc = "Location: " + str(self.location)
        gar = "At Garage: " + str(self.at_garage())
        stat = "Status: " + status

        print(sep + truck + dvr + loc + dvr + gar + "\n" + stat)
        # sys.stdout.flush()

    def find_route(self):
        """
        Finds the next path to take.
                - Note: It takes one iteration to drop off/pick up packages, and one turn to refuel
        :return:
        """
        if self.destination_reached():
            self.find_next_destination()
        else:
            self.follow_route()

    def find_next_destination(self):
        status = ""

        if self.idle() and not all_packages_are_being_delivered():
            status = 'Finding the next closest package'
            self.find_next_package()
        elif self.can_pickup_package():
            status = 'Picking up P' + str(self.next_package.ID) + ' and finding a path to its destination.'
            self.pickup_package()
        elif self.can_drop_off_package():
            status = 'Dropping off P' + str(self.package.ID)
            self.drop_off_package()
        elif all_packages_are_being_delivered():
            if self.at_garage():
                status = 'Waiting for other trucks to return'
            else:
                self.get_path_to(self.garage.location)
        else:
            print("YOU DIDN'T COVER ALL CASES.")

        self.print_status(status)

    def follow_route(self):
        """
        Follows the route and outputs the current status of the truck to the console
        :return: N/A
        """
        if not self.next_package_unknown() and self.empty():
            status = 'Navigating to package ' + str(self.next_package.location)
        elif self.next_package_unknown() and self.empty():
            status = 'Navigating to garage '
        else:
            status = 'Navigating to package\'s destination ' + str(self.package.destination)

        self.move()
        self.print_status(status)

    def move(self):
        """
        Goes along the route that is stored inside of the truck
        :return: N/A
        """
        self.distance_traveled += 1
        self.location = self.path.pop(0)
        if self.package is not None:
            self.package.location = self.location

    def get_path_to(self, destination):
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

    def find_next_package(self):
        search_time = 0

        for package in packages:
            problem = Problem(self.location, package.source, graph)
            search = AStar.search(problem)
            search_was_successful = search[0]
            search_time += search[3]
            if search_was_successful:
                path = search[1]
                path_cost = search[2]
                if path_cost < self.path_cost:
                    self.next_package = package
                    self.path_cost = path_cost
                    self.path = path
            else:
                print("Search could not find a path")

        add_time_spent_searching(search_time)
        packages.remove(self.next_package)
        packages_being_picked_up.append(self.next_package)
        print("Closest package: P" + str(self.next_package.ID) + " location " + str(self.next_package.location))


def create_graph():
    """
    Creates a map
    :return: the map that was created
    """
    g = Map.makeMap(map_width, map_height, map_noise)
    return g


def create_package(ID):
    """
    Creates a package and appends it to the list of packages
    :return: the initialized package
    """
    source = rand.choice(graph.nodes())
    destination = rand.choice(graph.nodes())
    package = Package(source, destination, ID, graph)
    add_time_spent_searching(package.time_spent_on_search)
    return package


def create_garage(ID):
    """
    Creates a new garage
    :return: The initialized garage
    """
    garage_location = rand.choice(graph.nodes())
    return Garage(garage_location, ID)


def create_truck(ID):
    """
    Creates a new truck
    :return: The newly created truck
    """
    garage = rand.choice(garages)
    truck = Truck(garage, range_of_truck, ID)
    return truck


def trucks_are_home():
    for garage in garages:
        if not garage.all_trucks_home():
            return False
    return True


def t_spent_searching():
    return timing_list[0]


def add_time_spent_searching(time_difference):
    timing_list[0] += time_difference


def all_packages_are_being_delivered():
    if len(packages) == 0:
        return True
    return False


packages = list()
packages_being_picked_up = list()
packages_in_transit = list()
delivered_packages = list()

trucks = list()
garages = list()

t_creating_graph = time.clock()
graph = create_graph()
t_creating_graph = time.clock() - t_creating_graph

# Create all of the packages
t_creating_packages = time.clock()
for num in range(0, number_of_packages):
    package = create_package(num)
    packages.append(package)
t_creating_packages = time.clock() - t_creating_packages
print("Created packages")

# Create all of the garages
t_creating_garages = time.clock()
for num1 in range(number_of_garages):
    garages.append(create_garage(num1))
t_creating_garages = time.clock() - t_creating_garages
print("Created garages")

# Create all of the trucks
t_creating_trucks = time.clock()
for num2 in range(number_of_trucks):
    trucks.append(create_truck(num2))
t_creating_trucks = time.clock() - t_creating_trucks
print("Created trucks")


def run_scenario():
    print("Running scenario:")
    iter = 0
    packages_to_deliver = len(packages)
    while packages_to_deliver != len(delivered_packages) and trucks_are_home():
        for truck in trucks:
            truck.find_route()
        if (draw_simulation):
            draw_paths(graph, garages, trucks, packages, packages_being_picked_up, packages_in_transit, iter)
        iter += 1
    return iter


iterations = run_scenario()
table_width = len('|----------------------------------|')
precision = 3

t_run_scenario = time.clock() - start_of_scenario
t_run_scenario = format_number_string('Total time: ', t_run_scenario, precision, table_width)
t_creating_graph = format_number_string('Graph creation: ', t_creating_graph, precision, table_width)
t_creating_packages = format_number_string('Making packages: ', t_creating_packages, precision, table_width)
t_creating_garages = format_number_string('Making garages: ', t_creating_garages, precision, table_width)
t_creating_trucks = format_number_string('Making trucks:', t_creating_trucks, precision, table_width)
t_spent_searching = format_number_string('Searching: ', t_spent_searching(), precision, table_width)

graph_dimensions = format_coordinate('Graph dimensions:', map_width, map_height, table_width)
graph_noise = format_string('Graph noise:', str(map_noise), table_width)
number_of_packages = format_string('Number of packages:', str(number_of_packages), table_width)
number_of_garages = format_string('Number of garages:', str(number_of_garages), table_width)
number_of_trucks = format_string('Number of trucks:', str(number_of_trucks), table_width)

print('\n\n')
print('\n\n')
print('|----------------------------------|')
print('| Problem variables                |')
print('|----------------------------------|')
print(graph_dimensions)
print(graph_noise)
print(number_of_packages)
print(number_of_trucks)
print(number_of_garages)
print('|----------------------------------|')
print('| TIME to complete                 |')
print('|----------------------------------|')
print(t_run_scenario)
print(t_creating_graph)
print(t_creating_packages)
print(t_creating_garages)
print(t_creating_trucks)
print(t_spent_searching)
print('|----------------------------------|')
if (make_gif):
    print('| MAKING GIF                       |')
    print('|----------------------------------|')
    giffify.create('sim', iterations)

