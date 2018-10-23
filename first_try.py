#!/usr/bin/env python3
# Python 3.6

import hlt
from hlt import constants
from hlt.positionals import Direction
import random
from utils import *


import logging
# Constants
MAXCARRY = 1000
RETURNTOBASE = 500

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
""" <<<Analyze Map and load models"""

ships = {}
"""<<<Enter Game>>>"""
game.ready("FirstTry")
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """


while True:
    game.update_frame()
    me = game.me
    game_map = game.game_map
    navigator = Navigator(game_map, me)

    command_queue = []

    for ship in me.get_ships():
        if ship.halite_amount > RETURNTOBASE:
            command_queue.append(ship.move(navigator.go_dropoff(ship)))
        elif game_map[ship.position].halite_amount < constants.MAX_HALITE / 10:
            command_queue.append(
                ship.move(
                    random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
        else:
            command_queue.append(ship.stay_still())

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)




