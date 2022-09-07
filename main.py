# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random2 as r
import typing
import strategy as s


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "MadJayhawk",
        "color": "#08ff08",
        "head": "beluga",
        "tail": "curled",
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START **")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    moves,direction = s.possible_moves(game_state)
    s.prt('moves',moves)
    s.prt('direction',direction)
    next_move = r.choice(direction)
    print("Next Move: ", next_move)
    # We've included code to prevent your Battlesnake from moving backwards
    # my_head = game_state["you"]["body"][0]  # Coordinates of your head
    # my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    # if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
    #     is_move_safe["left"] = False

    # elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
    #     is_move_safe["right"] = False

    # elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
    #     is_move_safe["down"] = False

    # elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
    #     is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']

    # Are there any safe moves left?

    safe_moves = ["right", "left", "up", "down"]

    # Choose a random move from the safe ones
    # next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"\nMOVE: {game_state['turn']}: {next_move}\n")
    return {"move": next_move}


# Start server when `python main.py is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
