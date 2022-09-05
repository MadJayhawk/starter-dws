#
import itertools as it
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import random2 as random


def prt(a, b):
    print(a, f":   {b}\n")


def find_closest(choices, coord):
    temp_closest = choices[0]
    temp_min_dist = pow(width, 2)
    for c in choices:
        a = abs(c[1] - coord[1])
        b = abs(c[0] - coord[0])
        distance = math.sqrt(pow(a, 2) + pow(b, 2))
        if distance < temp_min_dist:
            temp_min_dist = distance
            temp_closest = c
    return temp_closest


def find_the_snake_butts(hungry, snake_butts):
    # if there are more than two snakes
    if hungry or snake_butts == []:
        print("SNAKE BUTS IS " + str(snake_butts))
        print("im hungry")
        closest_food = find_closest(food, head)
        print("CLOSEST FOOD")
        print(closest_food)
        taunt_count = 0

        # another snake could be going for the same food
        # if not adjacent_square_safe(closest_food, data):
        #   print 'ADJACENT SQUARE NOT SAFE'
        #   if closest_food in safe_squares:
        #     safe_squares.remove(closest_food)

        best_move = find_closest(safe_squares, closest_food)
    # otherwise follow a snake
    else:
        closest_butt = find_closest(snake_butts, head)
        print("snake_butts", snake_butts)
        print("closest", closest_butt)


def possible_moves(data):

    head = data["you"]["head"]

    prt("head", head)
    moves = []
    direction = {}
    moves.append((head["x"] + 1, head["y"]))
    direction[(head["x"] + 1, head["y"])] = "right"
    moves.append((head["x"] - 1, head["y"]))
    direction[(head["x"] - 1, head["y"])] = "left"
    moves.append((head["x"], head["y"] + 1))
    direction[(head["x"], head["y"] + 1)] = "down"
    moves.append((head["x"], head["y"] - 1))
    direction[(head["x"], head["y"] - 1)] = "up"
    print(direction)
    return (
        moves,
        direction,
    )  # [R,L,U,D] from head position (2,5) --> [(3,5), (1,5), (2,6), (2,4)]


def get_snakes(data):
    s_all = []  # snake data [head, body - no head, length]
    for i in data["board"]["snakes"]:
        s_all.append(
            [
                (i["body"][:1][0]["x"], i["body"][:1][0]["y"]),
                [(a["x"], a["y"]) for a in i["body"][1:]],
                i["length"],
            ]
        )
        print(s_all)
    snakes = []
    for i in s_all:
        snakes += i[1]
    prt("snakes", snakes)
    prt("s_all", s_all)
    return (
        snakes,
        s_all,
    )  #  s_all= [head,body,length] and snakes = entire snake - all snakes


def in_snakes(moves, snakes_all):
    # test to see if head is in any snake including mySnake
    for i in moves:
        if i in snakes_all:
            moves.pop(moves.index(i))
    return moves


def in_walls(moves):
    for i in moves:
        if i[0] > 10 or i[0] < 0 or i[1] > 10 or i[1] < 0:
            moves.pop(moves.index(i))
    return moves


def find_food(data):
    food = []
    for i in data["board"]["food"]:
        food.append((i["x"], i["y"]))
    return food


def get_snakes(data):
    s_all = []  # snake data [head, body - no head, length]
    for i in data["board"]["snakes"]:
        s_all.append(
            [
                (i["body"][:1][0]["x"], i["body"][:1][0]["y"]),
                [(a["x"], a["y"]) for a in i["body"][1:]],
                i["length"],
            ]
        )
    snakes = []
    for i in s_all:
        snakes += i[1]
    prt("snakes", snakes)
    prt("s_all", s_all)
    return (
        snakes,
        s_all,
    )  #  s_all= [head,body,length] and snakes = entire snake - all snakes


def find_shortest_path(data):

    s, sn = get_snakes(data)
    myHead = sn[0][0]
    my_length = data["you"]["length"]
    print(f"\n\nsn: {sn}")
    enemy_heads = []
    for i in sn[1:]:
        enemy_heads.append((i[0], i[2]))
    print(f"\nenemy_heads: {enemy_heads}\n")
    hld_length = 1000
    shortest_path = []
    matrix = np.ones([11, 11], dtype=int)
    for i in s:  # snakes_all into matrix
        matrix[i[0], i[1]] = 0  # puts snakes' bodies in matrix
    print(matrix)
    for j in enemy_heads:
        if j[1] < my_length:
            grid = Grid(matrix=matrix)
            start = grid.node(myHead[0], myHead[1])  # sn[0][0] = my snake head
            end = grid.node(j[0][0], j[0][1])
            print(f"j: {j}   start: {myHead[0]} {myHead[1]} end: {j[0]} {j[1]}")
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)

            if len(path) < hld_length:
                hld_length = len(path)
                shortest_path = [path, j]
            print(f"path: {path}   hld_length: {hld_length}  len(path): {len(path)}")
            print(grid.grid_str(path=path, start=start, end=end))
            # print(f"\npath: {path}")
            print(
                f"\nshortest path: {shortest_path[0]}  path length: {shortest_path[1]}\n\n"
            )
    print(f"\n*****  shortest path:{shortest_path[0]}  ***** ")
    return shortest_path


def in_danger_snakes(data):
    danger = []
    my_length = data["you"]["length"]
    for i in data["board"]["snakes"]:
        if data["you"]["length"] < i["length"]:
            x = data["board"]["snakes"]["head"]
            danger.append((x[0], x[1]))
    return danger


def determine_move(data):
    moves, direction = possible_moves(data)  # four possible moves from current location
    snakes, snakes_all = get_snakes(
        data
    )  # snake data (head/body/length) and all snakes locations
    moves = in_walls(moves)  # is head touching wall
    if moves == []:
        quit()
    moves = in_snakes(moves, snakes_all)  # is head touching a snake
    if moves == []:
        quit()
    health = data["you"]["health"]
    if health > 80:
        avoid_food = True
    else:
        avoid_food = False
    food = find_food(data)
    shortest_path = find_shortest_path(data)
    print(f"\n\nshortest_path: {shortest_path}")
    print(f"\nMoves: {moves}\n\n")
    f = []
    for i in moves:
        if i in shortest_path[0]:
            f.append(direction[i])
    next_move = random.choice(f)
    return next_move


def game_data():
    data = {
        "board": {
            "height": 11,
            "width": 11,
            "food": [{"x": 0, "y": 6}, {"x": 5, "y": 7}, {"x": 4, "y": 9}],
            "snakes": [
                {
                    "body": [
                        {"x": 6, "y": 2},
                        {"x": 7, "y": 2},
                        {"x": 7, "y": 3},
                        {"x": 7, "y": 4},
                        {"x": 6, "y": 4},
                        {"x": 5, "y": 4},
                        {"x": 4, "y": 4},
                    ],
                    "head": {"x": 6, "y": 2},
                    "length": 7,
                },
                {
                    "body": [
                        {"x": 1, "y": 1},
                        {"x": 1, "y": 2},
                        {"x": 1, "y": 3},
                        {"x": 1, "y": 4},
                        {"x": 1, "y": 5},
                        {"x": 1, "y": 6},
                    ],
                    "head": {"x": 2, "y": 6},
                    "length": 6,
                },
                # {
                #     "body": [{"x": 3, "y": 4}, {"x": 3, "y": 5}, {"x": 3, "y": 6}],
                #     "head": {"x": 3, "y": 4},
                #     "length": 3,
                # },
                # {
                #     "body": [
                #         {"x": 8, "y": 8},
                #         {"x": 8, "y": 7},
                #         {"x": 8, "y": 6},
                #         {"x": 9, "y": 6},
                #         {"x": 9, "y": 5},
                #     ],
                #     "head": {"x": 8, "y": 8},
                #     "length": 5,
                # },
            ],
        },
        "you": {
            "health": 81,
            "body": [
                {"x": 6, "y": 2},
                {"x": 7, "y": 2},
                {"x": 7, "y": 3},
                {"x": 7, "y": 4},
                {"x": 6, "y": 4},
                {"x": 5, "y": 4},
                {"x": 4, "y": 4},
            ],
            "head": {"x": 6, "y": 2},
            "length": 7,
        },
    }
    return data


#
import itertools as it
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

import random2 as random


def prt(a, b):
    print(a, f":   {b}\n")


def possible_moves(data):

    head = data["you"]["head"]

    prt("head", head)
    moves = []
    direction = {}
    moves.append((head["x"] + 1, head["y"]))
    direction[(head["x"] + 1, head["y"])] = "right"
    moves.append((head["x"] - 1, head["y"]))
    direction[(head["x"] - 1, head["y"])] = "left"
    moves.append((head["x"], head["y"] + 1))
    direction[(head["x"], head["y"] + 1)] = "down"
    moves.append((head["x"], head["y"] - 1))
    direction[(head["x"], head["y"] - 1)] = "up"
    print(direction)
    return (
        moves,
        direction,
    )  # [R,L,U,D] from head position (2,5) --> [(3,5), (1,5), (2,6), (2,4)]


def get_snakes(data):
    s_all = []  # snake data [head, body - no head, length]
    for i in data["board"]["snakes"]:
        s_all.append(
            [
                (i["body"][:1][0]["x"], i["body"][:1][0]["y"]),
                [(a["x"], a["y"]) for a in i["body"][1:]],
                i["length"],
            ]
        )
        print(s_all)
    snakes = []
    for i in s_all:
        snakes += i[1]
    prt("snakes", snakes)
    prt("s_all", s_all)
    return (
        snakes,
        s_all,
    )  #  s_all= [head,body,length] and snakes = entire snake - all snakes


def in_snakes(moves, snakes_all):
    # test to see if head is in any snake including mySnake
    for i in moves:
        if i in snakes_all:
            moves.pop(moves.index(i))
    return moves


def in_walls(moves):
    for i in moves:
        if i[0] > 10 or i[0] < 0 or i[1] > 10 or i[1] < 0:
            moves.pop(moves.index(i))
    return moves


def find_food(data):
    food = []
    for i in data["board"]["food"]:
        food.append((i["x"], i["y"]))
    return food


def get_snakes(data):
    s_all = []  # snake data [head, body - no head, length]
    for i in data["board"]["snakes"]:
        s_all.append(
            [
                (i["body"][:1][0]["x"], i["body"][:1][0]["y"]),
                [(a["x"], a["y"]) for a in i["body"][1:]],
                i["length"],
            ]
        )
    snakes = []
    for i in s_all:
        snakes += i[1]
    prt("snakes", snakes)
    prt("s_all", s_all)
    return (
        snakes,
        s_all,
    )  #  s_all= [head,body,length] and snakes = entire snake - all snakes


def find_shortest_path(data):

    s, sn = get_snakes(data)
    myHead = sn[0][0]
    my_length = data["you"]["length"]
    print(f"\n\nsn: {sn}")
    enemy_heads = []
    for i in sn[1:]:
        enemy_heads.append((i[0], i[2]))
    print(f"\nenemy_heads: {enemy_heads}\n")
    hld_length = 1000
    shortest_path = []
    matrix = np.ones([11, 11], dtype=int)
    for i in s:  # snakes_all into matrix
        matrix[i[0], i[1]] = 0  # puts snakes' bodies in matrix
    print(matrix)
    for j in enemy_heads:
        if j[1] < my_length:
            grid = Grid(matrix=matrix)
            start = grid.node(myHead[0], myHead[1])  # sn[0][0] = my snake head
            end = grid.node(j[0][0], j[0][1])
            print(f"j: {j}   start: {myHead[0]} {myHead[1]} end: {j[0]} {j[1]}")
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)

            if len(path) < hld_length:
                hld_length = len(path)
                shortest_path = [path, j]
            print(f"path: {path}   hld_length: {hld_length}  len(path): {len(path)}")
            print(grid.grid_str(path=path, start=start, end=end))
            # print(f"\npath: {path}")
            print(
                f"\nshortest path: {shortest_path[0]}  path length: {shortest_path[1]}\n\n"
            )
    print(f"\n*****  shortest path:{shortest_path[0]}  ***** ")
    return shortest_path


def in_danger_snakes(data):
    danger = []
    my_length = data["you"]["length"]
    for i in data["board"]["snakes"]:
        if data["you"]["length"] < i["length"]:
            x = data["board"]["snakes"]["head"]
            danger.append((x[0], x[1]))
    return danger


def determine_move(data):
    moves, direction = possible_moves(data)  # four possible moves from current location
    snakes, snakes_all = get_snakes(
        data
    )  # snake data (head/body/length) and all snakes locations
    moves = in_walls(moves)  # is head touching wall
    if moves == []:
        quit()
    moves = in_snakes(moves, snakes_all)  # is head touching a snake
    if moves == []:
        quit()
    health = data["you"]["health"]
    if health > 80:
        avoid_food = True
    else:
        avoid_food = False
    food = find_food(data)
    shortest_path = find_shortest_path(data)
    print(f"\n\nshortest_path: {shortest_path}")
    print(f"\nMoves: {moves}\n\n")
    f = []
    for i in moves:
        if i in shortest_path[0]:
            f.append(direction[i])
    next_move = random.choice(f)
    return next_move


def game_data():
    data = {
        "board": {
            "height": 11,
            "width": 11,
            "food": [{"x": 0, "y": 6}, {"x": 5, "y": 7}, {"x": 4, "y": 9}],
            "snakes": [
                {
                    "body": [
                        {"x": 6, "y": 2},
                        {"x": 7, "y": 2},
                        {"x": 7, "y": 3},
                        {"x": 7, "y": 4},
                        {"x": 6, "y": 4},
                        {"x": 5, "y": 4},
                        {"x": 4, "y": 4},
                    ],
                    "head": {"x": 6, "y": 2},
                    "length": 7,
                },
                {
                    "body": [
                        {"x": 1, "y": 1},
                        {"x": 1, "y": 2},
                        {"x": 1, "y": 3},
                        {"x": 1, "y": 4},
                        {"x": 1, "y": 5},
                        {"x": 1, "y": 6},
                    ],
                    "head": {"x": 2, "y": 6},
                    "length": 6,
                },
                # {
                #     "body": [{"x": 3, "y": 4}, {"x": 3, "y": 5}, {"x": 3, "y": 6}],
                #     "head": {"x": 3, "y": 4},
                #     "length": 3,
                # },
                # {
                #     "body": [
                #         {"x": 8, "y": 8},
                #         {"x": 8, "y": 7},
                #         {"x": 8, "y": 6},
                #         {"x": 9, "y": 6},
                #         {"x": 9, "y": 5},
                #     ],
                #     "head": {"x": 8, "y": 8},
                #     "length": 5,
                # },
            ],
        },
        "you": {
            "health": 81,
            "body": [
                {"x": 6, "y": 2},
                {"x": 7, "y": 2},
                {"x": 7, "y": 3},
                {"x": 7, "y": 4},
                {"x": 6, "y": 4},
                {"x": 5, "y": 4},
                {"x": 4, "y": 4},
            ],
            "head": {"x": 6, "y": 2},
            "length": 7,
        },
    }
    return data
