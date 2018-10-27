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

    def update(self):
        self.game.update_frame()
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
                self.ships[ship.ship.id] = self.create_action_que(ship)
            command_que.append(self.perform_que_action(ship))
        self.game.end_turn(command_que)

    def create_action_que(self, ship):
        if ship.halite_amount > RETURNTOBASE:
            closest_dropoff = self.navigator.get_closest_off(ship.position, self.hr, self.navigator.dropoffs)
            return self.navigator.navigate_to(ship.position, closest_dropoff.position)
        elif False: # surround is attractive
            pass
        else:  # Move to closest honeyspot
            # rand.seed(ship.id)
            # ship_honey_spot = rand.choice(mpan.honey_spots[:TOPNSPOTS])
            closest_honey_spot = self.navigator.get_closest_off(ship.position, self.hr, self.mpan.honey_spots[:TOPNSPOTS])
            return self.navigator.navigate_to(ship.position, closest_honey_spot.position)
        return self.hr

    def perform_que_action(self, ship):
        action = self.ships[ship.id].pop()



class Task:

    def __init__(self):
        pass

    def next(self):
        return 1

class NavigationTask:
    pass

class FarmingTask:
    pass

class KillTask:
    pass

class InfraStrukturTask:
    pass

