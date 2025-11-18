""" Functions to handle ship creation, placement, and validation

    Functions:
        create_ship(name: str, length: int) -> dict:
            Create a ship with the specified name and length.
        
        place_ship(board: List[List[dict]], ship: dict, row: int, column: int, direction: str) -> bool:
            Place a ship on the board at the specified coordinates and direction.
        
        validate_ship_placement(board: List[List[dict]], ship: dict, row: int, column: int, direction: str) -> bool:
            Validate if a ship can be placed at the specified coordinates and direction.
"""
from typing import List, Tuple
import random
from gameBoard import cell_state


class Ship:
    def __init__(self, name: str, tile: str, length: int):
        """
        Create a ship with the specified name and length.
        
        Args:
            name (str): The name of the ship.
            tile (str): The tile representation of the ship.
            length (int): The length of the ship.
        """
        self.name:str = name # Name of the ship
        self.tile:str = tile # What ascii character is placed on the game board

        self.length:int = length
        self.bow_coord:Tuple[int, int] = None  # Bow coordinates of the ship, will be set when the ship is placed
        self.direction:str = None # Direction of the ship, can be 'up', 'down', 'left', or 'right'
        self.occupied_cells:list = []  # List to keep track of cells occupied by this ship

        self.hits:int = 0  # Number of hits the ship has taken
        self.is_sunk:bool = False # Indicates if the ship has been sunk, True when hits == length
        self.is_placed:bool = False # Indicates if the ship has been placed on the board, checks for bow_coord and direction and direction

    def __repr__(self):
        return f"Ship(name={self.name}, is_placed={self.is_placed}, is_sunk={self.is_sunk}"
    
    def place(self, board: List[List[dict]], row: int, column: int, direction: str, board_rows, board_columns) -> bool:
        """ Place the ship on the board at the specified coordinates and direction.
        Args:
            board (list): The game board where the ship will be placed.
            row (int): The row index where the ship's bow will be placed.
            column (int): The column index where the ship's bow will be placed.
            direction (str): The direction in which the ship will be placed ('up', 'down', 'left', 'right').
            board_dimensions (tuple): A tuple containing the dimensions of the board (rows, columns).

        Returns:
            bool: True if ship was succesfully placed
        """
        board_rows -= 1
        board_columns -= 1

        # Clear occupied tiles on the game board
        self.clear_ship(board)
        
        # Validate the coordinates and direction will put the ship within the board boundaries
        if direction not in ['up', 'down', 'left', 'right']:
            raise ValueError("Invalid direction. Must be 'up', 'down', 'left', or 'right'")
        
        if direction == 'up':
            if row - (self.length - 1) < 0: # self.length - 1 because row is the bow of the ship
                return False
            for i in range(self.length): # Check if the cells above the bow are occupied
                if board[row - i][column]['is_occupied']:
                    return False
            for i in range(self.length): # Place the ship on the board
                board[row - i][column]['is_occupied'] = True
                board[row - i][column]['tile'] = self.tile
                board[row - i][column]['ship'] = self
                self.occupied_cells.append((row - i, column))

        elif direction == 'down':
            if row + (self.length - 1) >= board_rows:
                return False
            for i in range(self.length):
                if board[row + i][column]['is_occupied']:
                    return False
            for i in range(self.length):
                board[row + i][column]['is_occupied'] = True
                board[row + i][column]['tile'] = self.tile
                board[row + i][column]['ship'] = self
                self.occupied_cells.append((row + i, column))

        elif direction == 'left':
            if column - (self.length - 1) < 0:
                return False
            for i in range(self.length):
                if board[row][column - i]['is_occupied']:
                    return False
            for i in range(self.length):
                board[row][column - i]['is_occupied'] = True
                board[row][column - i]['tile'] = self.tile
                board[row][column - i]['ship'] = self
                self.occupied_cells.append((row, column - i))

        elif direction == 'right': 
            if column + (self.length - 1) >= board_columns:
                return False
            for i in range(self.length):
                if board[row][column + i]['is_occupied']:
                    return False
            for i in range(self.length):
                board[row][column + i]['is_occupied'] = True
                board[row][column + i]['tile'] = self.tile
                board[row][column + i]['ship'] = self
                self.occupied_cells.append((row, column + i))

        self.bow_coord = (row, column)
        self.direction = direction
        self.is_placed = True
        return True # To indicate successful placement

    def random_place(self, board:List[List[dict]], board_rows:int, board_columns:int):
        """
        Randomly place a ship on the board.

        Args:
            ship: Ship object to set coordinates for.
            board: The game board the ship is being place on.
            board_rows: Number of rows the game board has.
            board_columns: Number of columns the game board has.

        Returns:
            bool: True if ship was succesfully place, if not place for whatever reason it will return False.
        """
        # Just uses the place function with a random direction and location chosen
        attempts:int = 0
        while True:
            attempts += 1
            random_row = random.randint(0, board_rows - 1)
            random_column = random.randint(0, board_columns - 1)
            direction_str = ('up', 'down', 'left', 'right')
            random_direction = direction_str[random.randint(0, 3)]
            if self.place(board, random_row, random_column, random_direction, board_rows, board_columns):
                break # If the ship is succesfully placed then exit the loop
            if attempts > 100:
                ValueError("Error: Bot cannot place ship randomly")

    def check_sunk(self) -> bool:
        """ Check if the ship is sunk. A ship is sunk if it has been hit as many times as its length.
        
        Returns:
            bool: True if the ship is sunk, False otherwise.
        """
        if self.hits >= self.length:
            self.is_sunk = True
            return True
        return False

    def clear_ship(self, board: List[List[dict]]):
        for coord in self.occupied_cells:
            board[coord[0]][coord[1]] = cell_state.copy()
        self.occupied_cells = [] # Clear if being replaced
        self.bow_coord = None
        self.direction = None
        self.is_placed = False

    def debug_print(self):
        """
        Debug and testing method to print out all the details of a ship
        """
        print(f"Name: {self.name}")
        print(f"Bow Coord: {self.bow_coord}")
        print(f"Direction: {self.direction}")
        print(f"Occupied Cells: {self.occupied_cells}")
        print(f"Hit Count: {self.hits}")
        print(f"is_placed: {self.is_placed}")
        print(f"is_sunk: {self.is_sunk}")
