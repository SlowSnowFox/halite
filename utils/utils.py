import hlt
from hlt import constants
from hlt.positionals import Direction, Position
import numpy as np
import networkx as nx
from itertools import product
import logging
import pickle
from itertools import product
import copy
# TODO if needed replace gmap.naive_navigate with a implementation that prioritizes ships with higher cargo


class Navigator:

    def __init__(self, gmap, me, heuristic, mpan):
        self.gmap = gmap
        self.me = me
        self.dropoffs = me.get_dropoffs() + [self.me.shipyard]
        self.mpan = mpan
        self.heuristic = heuristic
        self.heuristic.gmap = self.mpan.graph
        self.state_space = StateSpaceAnalyzer()

    def navigate_to(self, source, target):
        if source == target:
            return 'o'
        start = PositionConvertible.from_position(source)
        end = PositionConvertible.from_position(target)
        logging.info(f"Path Requested from {start.node} to {end.node}")
        path = nx.dijkstra_path(self.mpan.graph, start.node, end.node, self.heuristic)
        return path

    def get_closest_off(self, source, heuristic, elements):
        elements = [PositionConvertible.from_position(x.position) for x in elements]
        source = PositionConvertible.from_position(source)
        if elements:
            target = max(elements, key=lambda x: nx.shortest_path_length(self.mpan.graph,
                                                                       source=x.node,
                                                                       target=source.node,
                                                                       weight=heuristic))
            logging.info(f"got best node {target.node}")
            return target
        return None

    def farm_environment(self, ship):
        pc = PositionConvertible.from_position(ship.position)
        env = self.mpan.get_neighbourgraph(pc)
        graph = self.mpan.path_subgraph(env)
        adjgraph = self.mpan.convert_to_numpy(graph)
        path = self.state_space.sample_state_tree(adjgraph, 5)
        # convert the tuples to directions
        # convert the direction to a pathof pposition and stay stills
        return path

    def eval_environment(self, ship):
        pc = PositionConvertible.from_position(ship.position)
        env = self.mpan.get_neighbourgraph(pc)
        genv = self.mpan.graph.subgraph(env)
        return self.mpan.kernelheuristic(genv)


class MapAnalyzer:

    def __init__(self, gamemap, kernelheuristic):
        self.kernelheuristic = kernelheuristic
        self.gmap = gamemap
        self.graph = self.map_to_networkx()
        self.honey_spots = self.find_honey_spots()

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

    def find_honey_spots(self):
        height = self.gmap.height
        width = self.gmap.width
        h_spots = []
        for y in range(height):
            for x in range(width):
                pc = PositionConvertible.from_coordinates(x, y)
                sg = self.graph.subgraph(self.get_neighbourgraph(pc))
                h_spots.append(Kernel(pc, self.kernelheuristic(sg)))
        # TODO further evaluation of hotspots do something with overlapping regions
        return sorted(h_spots, key=lambda kernel: kernel.attractiveness, reverse=True)

    def update_graph(self):
        pass

    def get_neighbourgraph(self, pc):
        surr = set()
        for absoffset in range(self.kernelheuristic.size+1):
            for cell in product([0, -absoffset, absoffset], [0, -absoffset, absoffset]):
                surr.add(PositionConvertible.from_position(self.gmap.normalize(pc.position.directional_offset(cell))).node)
        return surr

    def convert_to_numpy(self, graph):
        return 1


class StateSpaceAnalyzer:

    def reward(self, halite, days):
        """
        :param halite: halite on the cell
        :param days: number of days you are planning on spennding there
        :return: mined amount subtracted by the leaving cost
        """
        return (1.1 * self.mined_t(days) - 0.1) * halite

    @staticmethod
    def mined_t(t):
        """
        :param t: t days spend on cell
        :return: percentage mined of cell
        """
        return 0.25 * np.array([np.power(0.75, x) for x in range(t)]).sum()

    @staticmethod
    def time_vs_reward(game_turn):
        return 1

    def sample_state_tree(self, graph, max_depth):
        # TODO only go back stepwise and not discard already computed results
        """
        :param graph: subgraph of the map as numpy matrix to perfom the analysis on
        :param starting_node: current position of the ship
        :param starting_halite: amount of halite ship currently has
        :param max_depth: max depth the function is going to explore
        :return: best path of farming and navigation to minimize the time needed to aquire threshold
        """
        options = [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]
        acc_halite = 0
        best = (1000*['o'])
        for path in product(*(max_depth * [options])):
            game_state = copy.deepcopy(graph)
            position = int(graph.size/2), int(graph.size/2)
            starting_halite = game_state[position[0]][position[1]]
            for depth, move in enumerate(path):
                if not self.is_valid(move, game_state, position):
                    break
                game_state, reward, position = self.evaluate(move, game_state, position)
                acc_halite += reward
                if acc_halite + starting_halite >= 900:
                    if depth < len(best):
                        best = path[:depth]
                    break
        return best

    @staticmethod
    def is_valid(move, graph, position):
        nodes = graph.nodes()
        min_node = min(nodes, key=lambda x: x.x + x.y)
        max_node = max(nodes, key=lambda x: x.x + x.y)
        position = PositionConvertible.from_node(position)
        position.x += move[0] % max_node.x+1
        position.y += move[1] % max_node.y+1
        if min_node.x <= position.x <= max_node.x or min_node.y <= position.y <= max_node.y:
            return True
        return False

    @staticmethod
    def evaluate(move, graph, position):
        if move == (0, 0):
            reward = graph[position[0]][position[1]] * 0.25
            graph[position] *= 0.75
            return graph, reward, position
        else:
            move_cost = graph[position[0]][position][1] * 0.1
            position.x += move[0] % 1  # mapsize
            position.y += move[1] % 1
            return graph, -move_cost, position


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


class Kernel:

    def __init__(self, core: PositionConvertible, attractiveness):
        self._attractiveness = attractiveness
        self.core = core
        self.ship_id = None
        self.nodes = None

    @property
    def position(self):
        return self.core.position

    @property
    def node(self):
        return self.core.node

    @property
    def attractiveness(self):
        return self._attractiveness
