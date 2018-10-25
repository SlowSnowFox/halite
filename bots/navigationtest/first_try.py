#!/usr/bin/env python3
# Python 3.6
import sys
sys.path.insert(0, "/home/norm/Documents/halite/halite/")

from bots.navigationtest.hyperparameter import *
from utils.utils import *
from utils.heuristic import *
import logging
#logging.basicConfig(filename="bot.log", level=logging.INFO)

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
    hr = Heuristic(HeuristicFunctions.distance_cost_adjusted, game_map)
    khr = KernelHeuristic(KernelHeuristicFunctions.absolute_sum, size=0)
    mpan = MapAnalyzer(game_map, khr)
    navigator = Navigator(game_map, me, hr, mpan)

    command_queue = []

    for ship in me.get_ships():
        next_command = ship.stay_still()
        if True:
            closest_honey_spot = navigator.get_closest_off(ship.position, hr, mpan.honey_spots)
            next_command = ship.move(navigator.navigate_to(ship.position, closest_honey_spot.position))

        command_queue.append(next_command)
    if game.turn_number <= BUILDTIME and me.halite_amount >= (constants.SHIP_COST + RESERVE) and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)




