#!/usr/bin/env python3
# Python 3.6
from .botinterface import *

game = hlt.Game()
rand = random.Random()
player = Bot(game)
game.ready("FirstTry")
while True:
    player.update()
    player.make_frame()




