#!/bin/sh
rm ./replays/*
./halite --replay-directory replays/ -vvv --width 32 --height 32 --no-logs "python3 ./bots/navigationtest/first_try.py" "python3 ./bots/randombot/MyBot.py"
rm bot-0.log
rm bot-1.log