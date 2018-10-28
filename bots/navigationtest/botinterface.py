#!/usr/bin/env python3
# Python 3.6
import sys
sys.path.insert(0, "/home/norm/Documents/halite/halite/")

from bots.navigationtest.hyperparameter import *
from utils.utils import *
from utils.heuristic import *
import logging
import random


class Bot:

    def __init__(self, game):
        # Long life onjects
        self.ships = {}
        self.game = game

        # Short  life objects
        self.me = game.me
        self.game_map = game.game_map
        self.hr = None
        self.khr = None
        self.mpan = None
        self.navigator = None
        self.placement_que = None  # lists all nodes that are going to be occupied by ships at the next move

        # testing object
        self.rand = random.Random()

    def update(self):
        self.game.update_frame()
        self.placement_que = set()
        self.me = self.game.me
        self.game_map = self.game.game_map
        self.hr = Heuristic(HeuristicFunctions.distance_cost_adjusted, self.game_map)
        self.khr = KernelHeuristic(KernelHeuristicFunctions.absolute_sum, size=0)
        self.mpan = MapAnalyzer(self.game_map, self.khr)
        self.navigator = Navigator(self.game_map, self.me, self.hr, self.mpan)

    def make_frame(self):
        command_que = []
        for ship in self.me.get_ships():
            if ship.id not in self.ships.keys():  # register new ship
                self.ships[ship.id] = []
            if not self.ships[ship.id]:  # means ship has no commands right now
                self.ships[ship.id] = self.create_action_que(ship)
            command_que.append(self.perform_que_action(ship))  # execute the next comman in the que
        if self.game.turn_number <= 200 and self.me.halite_amount >= constants.SHIP_COST + RESERVE and not self.game_map[self.me.shipyard].is_occupied:
            command_que.append(self.me.shipyard.spawn())  # if appropriate spawn ships
        self.game.end_turn(command_que)

    def create_action_que(self, ship):
        if ship.halite_amount > RETURNTOBASE:  #
            closest_dropoff = self.navigator.get_closest_off(ship.position, self.hr, self.navigator.dropoffs)
            path = self.navigator.navigate_to(ship.position, closest_dropoff.position)
            return self.create_nav_que(path)
        elif self.navigator.eval_environment(ship) > FARMING_THRESHOLD:  # farm surrounding area if its worth it
            path = self.navigator.farm_environment(ship)
            return self.create_farm_que(path)
        else:  # Move to closest honeyspot
            # self.rand.seed(ship.id)
            # closest_honey_spot = self.rand.choice(self.mpan.honey_spots[:TOPNSPOTS]) # hotfix so that not all of them go the same honeyspot
            closest_honey_spot = self.navigator.get_closest_off(ship.position, self.hr, self.mpan.honey_spots[:TOPNSPOTS])
            path = self.navigator.navigate_to(ship.position, closest_honey_spot.position)
            return self.create_nav_que(path)

    def perform_que_action(self, ship):
        pc = PositionConvertible.from_position(ship.position)
        task = self.ships[ship.id].pop(0)
        if isinstance(task, NavigationTask):
            relative_direction = self.get_relative_direction(task.source, task.target)
            enough_fuel = ship.halite_amount >= self.game_map[ship.position].halite_amount * 0.1  # check if ship can move
            is_free = task.target.node not in self.placement_que  # check if desired spot is occupied
            if enough_fuel and is_free:  # make the desired move
                self.placement_que.add(task.target.node)
                logging.info(f'{ship.id} will move to position {task.target.node}')
                logging.info(f'{self.placement_que} current status')
                return ship.move(relative_direction)
            else:
                self.placement_que.add(pc.node)
                self.ships[ship.id].insert(0, task)
                logging.info(f'{ship.id} wanted to move to {task.target.node} but could not because of {enough_fuel} fuel and {is_free}')
                return ship.stay_still()
        elif isinstance(task, FarmingTask):
            return 2
        elif isinstance(task, ScannerTask):
            return 3

    def create_nav_que(self, path):
        # TODO get rid of naive navigate hot fix
        que = []
        for i in range(1, len(path)):
            current = PositionConvertible.from_node(path[i-1])
            nextp = PositionConvertible.from_node(path[i])
            que.append(NavigationTask(current, nextp))
        return que

    def create_farm_que(self, path):
        return 2

    def get_relative_direction(self, source, target):
        # Modified code from hlt package can easily be refacored and condensed if some1 has time
        distance = abs(source.position - target.position)
        y_cardinality, x_cardinality = self.game_map._get_target_direction(source, target)
        possible_moves = []
        if distance.x != 0:
            possible_moves.append(x_cardinality if distance.x < (self.game_map.width / 2)
                                  else Direction.invert(x_cardinality))
        if distance.y != 0:
            possible_moves.append(y_cardinality if distance.y < (self.game_map.height / 2)
                                  else Direction.invert(y_cardinality))
        return possible_moves[0]

class Task:

    def __init__(self):
        pass

    def next(self):
        return 1


class NavigationTask:

    def __init__(self, source, target):
        self.target = target
        self.source = source


class FarmingTask:
    pass


class KillTask:
    pass


class InfraStrukturTask:
    pass


class ScannerTask:
    pass
