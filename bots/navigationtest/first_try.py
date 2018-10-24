#!/usr/bin/env python3
# Python 3.6
import sys
sys.path.insert(0, "/home/norm/Documents/halite/halite/")

from bots.navigationtest.hyperparameter import *
from utils.utils import *
from utils.heuristic import *


#import logging


""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
""" <<<Analyze Map and load models"""

ships = {}
"""<<<Enter Game>>>"""
game.ready("FirstTry")

""" <<<Game Loop>>> """


while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map
    hr = Heuristic(HeuristicFunctions.distance_naive, lambda x: x, game_map)
    navigator = Navigator(game_map, me, hr)

    command_queue = []

    for ship in me.get_ships():
        if True:
            command_queue.append(ship.move(navigator.navigate_to(ship.position, me.shipyard.position)))
        else:
            command_queue.append(ship.stay_still())

    if game.turn_number <= BUILDTIME and me.halite_amount >= (constants.SHIP_COST + RESERVE) and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)




