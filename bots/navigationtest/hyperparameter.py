# Direct Gameplay values
MAXCARRY = 1000  # Maximum amount of halite a ship can carry
RETURNTOBASE = 500  # Halite amount a ship needs after return to base is initialized
RESERVE = 1000  # If Halite Amount drops below the threshold no new ships are build
BUILDTIME = 200  # Number of turns the agents considers to build new ships

# Region attractiveness parameters
KERNELSIZE = 4  # size of the considered kernel
TIMEDISCOUNT = 0.8  # cell_value *0.8^n where n = n time steps to go there
