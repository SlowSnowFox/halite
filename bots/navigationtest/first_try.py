#!/usr/bin/env python3
# Python 3.6
import sys
sys.path.insert(0, "/home/norm/Documents/halite/halite/")

from bots.navigationtest.hyperparameter import *
from utils.utils import *
from utils.heuristic import *
import logging
import random

#logging.basicConfig(filename="bot.log", level=logging.INFO)

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
""" <<<Analyze Map and load models"""

ships = {}
"""<<<Enter Game>>>"""
game.ready("FirstTry")

""" <<<Game Loop>>> """
rand = random.Random()

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
        if ship.halite_amount > RETURNTOBASE:
            closest_dropoff = navigator.get_closest_off(ship.position, hr, navigator.dropoffs)
            next_command = ship.move(navigator.navigate_to(ship.position, closest_dropoff.position))
        elif game_map[ship.position].halite_amount > 400:
            next_command = ship.stay_still()
        elif random.randint(0, 100) < 4:  # move in random directions sometimes so that they dont get stuck
            next_command = ship.move(random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ]))
        else:
            rand.seed(ship.id)
            ship_honey_spot = rand.choice(mpan.honey_spots[:TOPNSPOTS])
            # closest_honey_spot = navigator.get_closest_off(ship.position, hr, mpan.honey_spots[:TOPNSPOTS])
            next_command = ship.move(navigator.navigate_to(ship.position, ship_honey_spot.position))
        command_queue.append(next_command)
    if game.turn_number <= BUILDTIME and me.halite_amount >= (constants.SHIP_COST + RESERVE) and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    game.end_turn(command_queue)




