#!/bin/sh
rm ./replays/*
./halite --replay-directory replays/ -vvv --width 32 --height 32 --turn-limit 30 --no-logs "python3 ./bots/navigationtest/first_try.py" "python3 ./bots/randombot/MyBot.py"
mv ./bot-0.log ./replays/botlogs/
mv ./bot-1.log ./replays/botlogs/