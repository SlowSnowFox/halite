import numpy as np
import networkx as nx
# TODO maybe normalize heuristics when adding them together


class Heuristic:

    def __init__(self, heuristic, nmap, weight=1):
        self.distance = heuristic
        self.gmap = nmap
        self.weight = weight

    def __call__(self, p1, p2, dirt=None):
        return self.distance(p1, p2, self.gmap)

    def __add__(self, other):
        reshr = lambda p1, p2, dirt=None: self.distance(p1, p2)*self.weight + other.distance(p1, p2) * other.weight
        return Heuristic(reshr, self.gmap)


class HeuristicFunctions:

    @staticmethod
    def distance_naive(source, target, map):
        return 1

    @staticmethod
    def distance_cost_adjusted(source, target, map):
        return map.nodes[source].get("halite")*0.1


class KernelHeuristic:

    def __init__(self, heuristic, size):
        self.heuristic = heuristic
        self.size = size

    def __call__(self, subnetwork):
        return self.heuristic(subnetwork)

    def __add__(self, other):
        # TODO
        return 1


class KernelHeuristicFunctions:

    @staticmethod
    def absolute_sum(kernel):
        halite = nx.get_node_attributes(kernel, "halite").values()
        return sum(halite)
