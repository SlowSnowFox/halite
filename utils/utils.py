import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import numpy as np
import networkx as nx
# TODO if needed replace gmap.naive_navigate with a implementation that prioritizes ships with higher cargo


class Navigator:

    def __init__(self, gmap, me, heuristic):
        self.gmap = gmap
        self.me = me
        self.dropoffs = me.get_dropoffs() + [self.me.shipyard]
        self.mpan = MapAnalyzer(gmap)
        self.heuristic = heuristic

    def navigate_to(self, source, target):
        start = PositionConvertible.from_position(source)
        end = PositionConvertible.from_position(target)
        path = nx.dijkstra_path(self.mpan.graph, start.node, end.node, self.heuristic)
        next_step = PositionConvertible.from_node(path[0])
        save_target = next_step.position
        return self.gmap.navigate_naive(source, save_target)

    def get_closest_off(self, p2, heuristic, elements):
        positions = 1
        if elements:
                return max(elements, lambda x: nx.shortest_path_length(self.gmap, p2.node, x.node, heuristic))
        return None


class MapAnalyzer:

    def __init__(self, gamemap):
        self.gmap = gamemap
        self.graph = self.map_to_networkx()

    def find_global_best_spots(self):
        pass

    def map_to_networkx(self):
        height = self.gmap.height
        width = self.gmap.width
        g = nx.Graph()
        edges = []
        nodes = {}
        for y in range(height):
            for x in range(width):
                pc = PositionConvertible.from_coordinates(x, y)
                neighbours = [PositionConvertible.from_position(pos).node for pos in pc.position.get_surrounding_cardinals()]
                edges += [(startnode, endnode) for startnode, endnode in zip([pc.node]*4, neighbours)]
                nodes[pc.node] = self.gmap[pc.position].halite_amount
        g.add_edges_from(edges)
        nx.set_node_attributes(g, nodes, name="halite")
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


class Region:

    def __init__(self, position1, position2):
        self.upper_x = position1.x
        self.upper_y = position1.y

    def something(self):
        pass

