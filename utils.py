import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import numpy as np
import networkx as nx
# TODO if needed replace gmap.naive_navigate with a implementation that prioritizes ships with higher cargo


class Navigator:

    def __init__(self, gmap, me):
        self.gmap = gmap
        self.me = me
        self.dropoffs = me.get_dropoffs()
        self.mpan = MapAnalyzer(gmap)

    def go_to_closest_dropoff(self, ship, heuristic="naive"):
        nearest_dropoff = self.get_closest_dropoff(ship.position, heuristic)
        if heuristic == "naive":
            return self.navigate_naive(ship, nearest_dropoff)
        if heuristic == "cost_adjusted":
            return self.navigate_cost_adjusted(ship, nearest_dropoff)

    def get_closest_dropoff(self, position, heuristic):
        if self.dropoffs:
            if heuristic == "naive":
                return max(self.dropoffs, key=lambda dps: self.distance_naive(dps.position, position))
            elif heuristic == "cost_adjusted":
                return max(self.dropoffs, key=lambda dps: self.distance_cost_adjusted(dps.position, position))
        else:
            return self.me.shipyard.position

    def find_local_best_spot(self, ship, vision_range=5, distance_discount=0.1):
        """
        finds the best local position for a ship
        :param ship:
        :param vision_range:
        :param distance_discount:
        :return: position
        """
        def calc_reward(distance, amount):
            return amount - distance*distance_discount*1
        cell = self.gmap[ship.position]
        max(self.get_environment(cell, vision_range), key=lambda x: x)
        return 2

    def get_environment(self, position, vision_range):

        return {"distance": 2, "amaount": 30}

    def distance_naive(self, source, target):
        return self.gmap.calculate_distance(source, target)

    def distance_cost_adjusted(self, position1, position2):
        start = PositionConvertible.from_position(position1).node
        end = PositionConvertible.from_position(position2).node
        return nx.shortest_path_length(self.mpan.graph, start, end)

    def navigate_naive(self, ship, target):
        return self.gmap.naive_navigate(ship, target)

    def navigate_cost_adjusted(self, ship, target):
        start = PositionConvertible.from_position(ship.position).node
        end = PositionConvertible.from_position(target).node
        path = nx.dijkstra_path(self.mpan.graph, start, end)
        next_step = PositionConvertible.from_node(path[0])
        save_target = next_step.position
        return self.navigate_naive(ship, save_target)


class MapAnalyzer:

    def __init__(self, gamemap):
        self.gmap = gamemap
        self.graph = self.map_to_networkx()

    def find_global_best_spots(self):
        pass

    def map_to_networkx(self):
        height = self.gmap.height
        width = self.gmap.width
        g = nx.DiGraph()
        edges = []
        for y in range(height):
            for x in range(width):
                pc = PositionConvertible.from_coordinates(x,y)
                travel_cost = self.gmap[pc.position].halite_amount * 0.1
                neighbours = [PositionConvertible.from_position(pos).node for pos in pc.position.get_surrounding_cardinals()]
                edges += [(startnode, endnode, travel_cost) for startnode, endnode in zip([pc.node]*4, neighbours)]
        g.add_weighted_edges_from(edges)
        return g

    def update_graph(self):
        pass

    def identify_dropoffs(self):
        pass


class PositionConvertible:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_position(cls, pos):
        return cls(pos.x, pos.y)

    @classmethod
    def from_node(cls, node):
        return cls(int(node[0:3]), int(node[4:]))  # x takes 3 places and the y starts at , should be faster than regex

    @classmethod
    def from_coordinates(cls, x, y):
        return cls(x, y)

    @property
    def position(self):
        return Position(self.x, self.y)

    @property
    def node(self):
        num_zeros = 3 - len(str(self.x))  # max 3 digit height and width
        return f'{num_zeros}{self.x}, {self.y}'
