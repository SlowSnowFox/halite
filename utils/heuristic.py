class Heuristic:

    def __init__(self, distance, time_discount, nmap):
        self.distance = distance
        self.time_discount = time_discount
        self.gmap = nmap

    def __call__(self, p1, p2, dirt=None):
        return self.distance(p1, p2, self.gmap)

    def __add__(self, other):
        return 2


class HeuristicFunctions:

    @staticmethod
    def distance_naive(source, target, map):
        return 1

    @staticmethod
    def distance_cost_adjusted(source, target, map):
        return map.nodes[source].get("halite")*0.1

