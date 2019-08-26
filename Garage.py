__author__ = 'Mike Graham'
__email__ = 'michael.graham@usask.ca'
__date__ = 'February 2, 2016'

class Garage:
    """
    The garage class is used to represent a garage
    """

    def __init__(self, location, ID):
        self.ID = ID
        self.location = location
        self.trucks = []

    def add_truck(self, truck):
        self.trucks.append(truck)

    def remove_truck(self, truck):
        self.trucks.remove(truck)

    def all_trucks_home(self):
        for truck in self.trucks:
            if not truck.at_garage():
                return False
        return True