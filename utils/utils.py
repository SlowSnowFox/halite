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
        self.heuristic.gmap = self.mpan.graph

    def navigate_to(self, source, target):
        if source == target:
            return 'o'
        start = PositionConvertible.from_position(source)
        end = PositionConvertible.from_position(target)
        path = nx.dijkstra_path(self.mpan.graph, start.node, end.node, self.heuristic)
        next_step = PositionConvertible.from_node(path[1])
        save_target = next_step.position
        source.position = source  # needed because naive navigate only takes ships and not positions as first input
        return self.gmap.naive_navigate(source, save_target)

    def get_closest_off(self, p2, heuristic, elements):
        positions = 1
        if elements:
                return max(elements, lambda x: nx.shortest_path_length(self.gmap, p2.node, x.node, heuristic))
        return None


class MapAnalyzer:

    def __init__(self, gamemap):
        self.gmap = gamemap
        self.graph = self.map_to_networkx()
        self.matrix = self.map_to_np()

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
                neighbours = [self.gmap.normalize(pos) for pos in pc.position.get_surrounding_cardinals()]
                neighbours = [PositionConvertible.from_position(pos).node for pos in neighbours ]
                edges += [(startnode, endnode) for startnode, endnode in zip([pc.node]*4, neighbours)]
                g.add_node(pc.node)
                nodes[pc.node] = self.gmap[pc.position].halite_amount
        g.add_edges_from(edges)
        nx.set_node_attributes(g, nodes, name="halite")
        return g

    def map_to_np(self):

        return 1

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
        # return cls(int(node[0:3]), int(node[4:]))  # x takes 3 places and the y starts at , should be faster than regex
        delindex = node.index(",")
        return cls(int(node[0:delindex]), int(node[delindex+1:]))

    @classmethod
    def from_coordinates(cls, x, y):
        return cls(x, y)

    @property
    def position(self):
        return Position(self.x, self.y)

    @property
    def node(self):  # networkx needs a hashable type
        pad_zeros = '0' * (3 - len(str(self.x)))  # max 3 digit height and width
        return f'{pad_zeros}{self.x}, {self.y}'


class Region:

    def __init__(self, position1, position2):
        self.upper_x = position1.x
        self.upper_y = position1.y

    def something(self):
        pass

