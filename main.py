# battleships game
# written by julian beggs, august 2023

import random
from pprint import pprint as pprint

# Constants
SIZE = 15
SHIPS = [
    {"name": "Carrier", "size": 5},
    {"name": "Battleship", "size": 4},
    {"name": "Cruiser", "size": 3},
    {"name": "Submarine", "size": 3},
    {"name": "Destroyer", "size": 2}
]


def initialize_game():
    '''Run once at start of new game. Create new grid with ships placed randomly.'''
    print("initialize_game")

    rows = SIZE
    cols = SIZE
    board = [[0 for col in range(cols)]
             for row in range(rows)]  # board filled with 0
    # pprint(board)
    ships = SHIPS.copy()

    for ship in ships:
        name = ship["name"]
        size = ship["size"]
        ship["position"] = None

        # try to update board with ship at random position
        while ship["position"] is None:
            (row, col) = (random.randint(0,rows-1), random.randint(0,cols-1))
            orientation = random.randint(0, 1)  # 0 horizontal, 1 vertical
            position = ship["position"] = insert_ship(name, size, orientation, row, col, board)
            #TODO: fix the position to include row & col

            if bool(orientation):
                ship["orientation"] = "vertical" 
            else: ship["orientation"] = "horizontal"
            orientation = ship["orientation"]
            
        print(f"{name} sailing {orientation} at: {position}.")


def insert_ship(name, size, orientation, row, col, board):
    '''update board with ship, returns ships position or None if ship does not fit on board or overlaps existing.'''
    print("insert_ship", name)
    # check if ship position fits on board without overlap
    if orientation == 0:  # horizontal case so row fixed, iterate columns

        if col+size > SIZE-1 or col-size < 0:
            return None  # ship doesn't fit on board

        overlap_left = overlap_right = 0
        for c in range(col, col+size):         # check going right from col
            overlap_right += board[row][c]
        for c in range(col-size, col):        # check going left from col
            overlap_left += board[row][c]

        ship_pos = None
        if overlap_left > 0 and overlap_right > 0:
            return ship_pos  # ship doesn't fit at selected position
        elif overlap_left == 0:
            ship_pos = [c for c in range(col-size, col)]
        elif overlap_right == 0:
            ship_pos = [c for c in range(col, col+size)]
        # print(ship_pos)
        return ship_pos

    elif orientation == 1:  # vertical case so column fixed, iterate rows

        if row+size > SIZE-1 or row-size < 0:
            return None  # ship doesn't fit on board

        overlap_down = overlap_up = 0
        for r in range(row, row+size):         # check going down from row
            overlap_down += board[r][col]
        for r in range(row-size, row):        # check going up from row
            overlap_up += board[r][col]

        ship_pos = None
        if overlap_down > 0 and overlap_up > 0:
            return ship_pos  # ship doesn't fit at selected position
        elif overlap_up == 0:
            ship_pos = [r for r in range(row-size, row)]
        elif overlap_down == 0:
            ship_pos = [r for r in range(row, row+size)]
        # print(ship_pos)
        return ship_pos


def player_turn():
    '''On each turn, get coordinates from player. Check if hit or miss, hit and sunk, update indicators and progress display'''

    pass


def player_wins():
    '''Check if 5 ships sunk => Player wins True else false'''

    pass


if __name__ == "__main__":
    initialize_game()
    # while not player_wins():
    #     player_turn()
