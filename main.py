# battleships game
# written by julian beggs, august 2023

import os
import random
from pprint import pprint

# Constants
BOARD_SIZE = 15
SHIPS = [
    {"name": "Carrier", "size": 5},
    {"name": "Battleship", "size": 4},
    {"name": "Cruiser", "size": 3},
    {"name": "Submarine", "size": 3},
    {"name": "Destroyer", "size": 2}
]


def initialize_game():
    '''Run once at start of new game. Create new grid with ships placed randomly.'''

    for i in range(3): print()
    print("Starting a new game.")
    print(f"The game board is a square of {BOARD_SIZE} position each side.")
    print("Locating current position of ships in the fleet...")

    rows = BOARD_SIZE
    cols = BOARD_SIZE
    ships = SHIPS.copy()
    fleet_board = [[0 for col in range(cols)] for row in range(rows)]  # new board filled with 0s
    game_board = [[0 for col in range(cols)] for row in range(rows)]  # new board filled with 0s

    for ship in ships:
        name = ship["name"]
        size = ship["size"]
        ship["damage"] = 0
        ship["status"] = "SAILING"

        # try to update board with ship at random position
        ship["position"] = None
        while ship["position"] is None:
            (row, col) = (random.randint(0, rows-1), random.randint(0, cols-1))
            orientation = ship["orientation"] = "V" if random.randint(
                0, 1) else "H"
            position, fleet_board = insert_ship(
                name, row, col, orientation, size, fleet_board)
            ship["position"] = position
        print()
        print(f"{name} sailing at: {position[0]+1, position[1]+1}.")
    
    return ships, fleet_board, game_board


def insert_ship(name, row, col, orientation, size, fleet_board):
    '''returns updated board with ship inserted or None if ship couldn't be inserted at position.
    row, col is starting position. place "size" positions either by row (H) or by col (V).'''
    print(f"Locating {name}... ", end="")

    # check if ship position fits on board and without overlapping existing ship

    ship_pos = None
    if orientation == "H":  # horizontal case so row fixed, iterate columns

        # check ship can be placed on board row
        if col+size > BOARD_SIZE-1 or col-size < 0:
            return ship_pos, fleet_board  # ship doesn't fit on board at col.

        # check if it will overlap existing ship
        overlap_dec = overlap_inc = 0
        for c in range(col, col+size, 1):         # check increasing from col
            overlap_inc += fleet_board[row][c]
        for c in range(col, col-size, -1):        # check decreasing from col
            overlap_dec += fleet_board[row][c]

    elif orientation == "V":  # vertical case so column fixed, iterate rows

        # check ship can be placed on board row
        if (row+size > BOARD_SIZE-1 or row-size < 0):
            return ship_pos, fleet_board  # ship doesn't fit on board at row.

        # find overlap with existing ship
        overlap_dec = overlap_inc = 0
        for r in range(row, row+size, 1):         # check increasing from row
            overlap_inc += fleet_board[r][col]
        for r in range(row, row-size, -1):        # check decreasing from row
            overlap_dec += fleet_board[r][col]

    if overlap_dec > 0 and overlap_inc > 0:
        return ship_pos, fleet_board  # ship doesn't fit at selected position
    elif overlap_inc == 0:
        ship_pos = [row, col, orientation, size]
    elif overlap_dec == 0:
        if orientation == "H":
            col -= size
        if orientation == "V":
            row -= size
        ship_pos = [row, col, orientation, size]

    # update board with inserted ship
    if orientation == "H":
        for c_ in range(col, col+size):
            fleet_board[row][c_] = 1
    if orientation == "V":
        for r_ in range(row, row+size):
            fleet_board[r_][col] = 1

    return ship_pos, fleet_board

def player_turn(ships, fleet_board, game_board):
    '''On each turn, get coordinates from player. Check if hit or miss, hit and sunk, update indicators and progress display'''

    # get target coords
    xcoord, ycoord = get_target_coords() # coord 1-indexed
    row = xcoord -1; col = ycoord -1    # convert to 0 indexed row, col
    
    #Check if hit or miss
    ships, fleet_board, game_board = is_hit(row, col, ships, fleet_board, game_board)

    # Check if ship sunk
    for ship in ships:
        if ship['damage'] == ship['size'] and ship['status'] != "SUNK":
            print(f"{ship['name']} has been sunk!! Well done!!")
            ship['status'] = "SUNK"
    
    return ships, fleet_board, game_board
        
def get_target_coords():
    '''On each turn, get coordinates from player.'''

    # get target coordinates
    coords_valid = False
    while not coords_valid:
        try:
            xcoord, ycoord = input(
                "Please enter target coordinates eg. 5 7  => ").split(" ")
            xcoord = int(xcoord)  # will raise error if cannot be cast to int
            ycoord = int(ycoord)
            if (xcoord in range(1, BOARD_SIZE+1) and ycoord in range(1, BOARD_SIZE+1)):
                coords_valid = True
            else:
                raise ValueError
        except ValueError:
            print(
                f"Try Again. Enter two integers between 1 and {BOARD_SIZE} separated by a single space.")
            coords_valid = False

    os.system('clear') # clear the Screen
    print(f"Firing on: {xcoord}, {ycoord}")
    return xcoord, ycoord
    

def is_hit(row, col, ships, fleet_board, game_board):
    '''check is coords hit ship and if so update ships damage/sunk status'''
    
    shot_hit = fleet_board[row][col] > 0
    if shot_hit:
        # which ship got hit
        for ship in ships:
            ship_rowcols = get_ship_rowcols(ship["position"])
            if (row, col) in ship_rowcols:
                print(f"{ship['name']} has been hit at ({row+1}, {col+1})")
                # update ship damage
                ship['damage'] += 1
                print(f"{ship['name']} has {ship['size']-ship['damage']} points left.")
                # update board with hit indicator
                game_board[row][col] = 6
    else:
        print(f"That's a miss at ({row+1}, {col+1})")
        # update board with miss indicator
        game_board[row][col] = 9

    return ships, fleet_board, game_board

def get_ship_rowcols(ship_pos):
    row, col, orientation, size = ship_pos
    ship_rowcols = []
    if orientation == "H": # iterate cols
        for c in range(col, col+size):
            ship_rowcols.append((row, c))
    if orientation == "V": # iterate rows
        for r in range(row, row+size):
            ship_rowcols.append((r, col))
    return ship_rowcols

def gameover(ships):
    '''Display updated game status message.'''
    total_fleet_size = total_fleet_damage = 0
    for ship in ships:
        total_fleet_size +=ship['size']
        total_fleet_damage +=ship['damage']
    
    for ship in ships:
        print(f"SHIP:{ship['name']} DAMAGE:{ship['damage']}/{ship['size']} STATUS:{ship['status']}")
        
    print(f"Game progress: {total_fleet_damage}/{total_fleet_size}")

    return True if total_fleet_damage == total_fleet_size else False


if __name__ == "__main__":
    ships, fleet_board, game_board = initialize_game()
    while not gameover(ships):
        player_turn(ships, fleet_board, game_board)
        for i in range(2): print()
