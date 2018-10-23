import hlt
from hlt import constants
from hlt.positionals import Direction


class Navigator:

    def __init__(self, gmap, me):
        self.gmap = gmap
        self.me = me
        self.dropoffs = me.get_dropoffs()

    def go_to_closest_dropoff(self, ship):
        return self.gmap.naive_navigate(ship, self.get_closest_dropoff(ship).id)

    def get_closest_dropoff(self, ship):
        return max(self.dropoffs, key=lambda x: self.distance_naive(x, ship))

    def save_navigate(self):
        return 1

    def distance_naive(self, source, target):
        return self.gmap.calculate_distance(source, target)

    def distance_cost_adjusted(self):
        return 2