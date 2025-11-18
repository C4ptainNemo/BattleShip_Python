""" Functions for controlling the bot's actions in the game """

from typing import List, Tuple
import random

class Bot:
    """
    Class to represent the bot in the game.
    
    Attributes:
        name (str): The name of the bot.
        board (List[List[dict]]): The game board for the bot.
    """
    
    def __init__(self, name: str, rows: int, columns: int):
        """
        Initialize the bot with a name and a game board.
        
        Args:
            name (str): The name of the bot.
            rows (int): Number of rows in the game board.
            columns (int): Number of columns in the game board.            
        """
        self.name = name
        self.rows = rows
        self.columns = columns
        
        self.checkboard_pattern = [] # Generate the checkboard pattern for attacks
        self.adjactent_pattern = []  # Placeholder for adjacent pattern, can be generated later if needed
        self.search_generate()  # Generate the search patterns upon initialization

        self.hunt_mode_active = False  # Flag to indicate if the bot is in hunt mode
        self.first_hit: Tuple[int, int] = None  # Coordinates of the first hit, used in hunt mode
        self.last_hit: Tuple[int, int] = None  # Coordinates of the last hit, used in hunt mode
        self.last_shot_hit: bool = False  # Falg to indicate if the last shot hit a ship
        self.hunt_direction: int = None  # Search direction in hunt mode, can be 0 (up), 1 (down), 2 (left), or 3 (right)

    def search_generate(self) -> Tuple[int, int]:
        """
        Generates search patterns for different stages of the game.
        1: Checkboard pattern is used for the initial search. It has 2 column spaces between attacks in a checkboard pattern. Pattern is randomly shifted slightly to avoid predictability.
        2: Spaces where there are two adjactent tiles not in the checkboard pattern.
        Bot should then resort to random attacks of remaining tiles.
        
        Returns:
            Tuple[int, int]: Row and column of shot.
        """
        
        # 1: Checkboard pattern.
            # Define the spaces between attacks, this is to make it easier to adjust later if needed.
            # Add some jiggle to offset the pattern slightly to avoid predictability.
        # 2: Adjacent tiles pattern.
            # Adjacent tiles are defined as two tiles that are not in the checkboard pattern.
            # In the diagram below, C are the tiles in the checkboard pattern, A are the tiles in the adjacent pattern, and ~ tiles not in a pattern.
            # The idea is that the smallest ship can fit into the gaps between the checkboard pattern, but hopefully gets found by it. If not the the adjacent pattern will find it.
            # The adjacent pattern is on the first and third row of every three rows. The first row covers left and down, the third row covers right and up.
            # The pattern looks like this:
            # # 0 1 2 3 4 5
            # 0 C ~ A C ~ A
            # 1 ~ C ~ ~ C ~
            # 2 A ~ C A ~ C
            # 3 C ~ A C ~ A
            # 4 ~ C ~ ~ C ~
            # 5 A ~ C A ~ C
        
        checkboard_spacing = 2  # Spaces between attacks in the checkboard pattern
        jiggle = random.randint(0, checkboard_spacing)  # Randomly shift the pattern slightly to avoid predictability
        checkboard_coordinates = [] # List to hold the coordinates in a checkboard pattern
        adjactent_coordinates = [] # List to hold the coordinates of adjacent tile pattern
        for row in range(self.rows):
            start = row % 3 - jiggle # Adjust the start index based on the row and jiggle value, negate so first acceptable value is 0, 1 or 2
            for i in range(0, self.columns, checkboard_spacing + 1):  # Iterate through the columns with the specified spacing
                # 1: Get column for checkboard pattern
                col = start + i
                if col >= 0 and col < self.columns:  # If column index is in bounds append to checkboard coordinate list
                    checkboard_coordinates.append((row, col))

                # 2: Get column for adjacent tiles, reference above for explanation of row type.
                row_type = row % 3
                if row_type == 0:
                    col = start + i + 2
                elif row_type == 1:
                    continue
                elif row_type == 2:
                    col = start + i + 1

                if col >= 0 and col < self.columns:  # If column index is in bounds append to checkboard coordinate list
                    adjactent_coordinates.append((row, col))

        self.checkboard_pattern = checkboard_coordinates
        self.adjactent_pattern = adjactent_coordinates

    def hunt_mode(self, board: List[List[dict]]) -> Tuple[int, int]:
        """
        In hunt mode, bots has hit a ship and is now trying to find the rest of it.

        Args:
            board (List[List[dict]]): The game board where the bot is searching for the ship.
        
        Returns:
            Tuple[int, int]: Row and column of shot.
        """
        attempt: int = 0  # Counter for how many times bot has tried to find valid shot

        if self.hunt_direction is not None: # If the last shot hit a ship, continue in the same direction
            direction_reversed_flag = False  # Flag to indicate if the direction has been reversed
            while True:
                attempt += 1
                # Determine the next shot based on the hunt direction
                if self.hunt_direction == 0:  # Up
                    shot_row = self.last_hit[0] - 1
                    shot_column = self.last_hit[1]
                elif self.hunt_direction == 1:  # Down
                    shot_row = self.last_hit[0] + 1
                    shot_column = self.last_hit[1]
                elif self.hunt_direction == 2:  # Left
                    shot_row = self.last_hit[0]
                    shot_column = self.last_hit[1] - 1
                elif self.hunt_direction == 3:  # Right
                    shot_row = self.last_hit[0]
                    shot_column = self.last_hit[1] + 1

                # Check if the shot is within bounds and not already shot at, if so return the coordinates
                if (0 <= shot_row < self.rows and
                    0 <= shot_column < self.columns and
                    not board[shot_row][shot_column]["is_shot"]):
                    # If the next shot is valid, update the last hit and return the coordinates
                    return (shot_row, shot_column)
                else:
                    # If the next shot is out of bounds or already shot at, reverse the direction
                    if not direction_reversed_flag:
                        self.hunt_direction = 1 if self.hunt_direction == 0 else 0 if self.hunt_direction == 1 else 3 if self.hunt_direction == 2 else 2
                        direction_reversed_flag = True
                        self.last_hit = self.first_hit # Go back to first hit and look other way
                    # If it has already been reversed, change direction
                    else:
                        self.hunt_direction = (self.hunt_direction + 2) % 4
                        direction_reversed_flag = False
                
                if attempt > 100: # If the bot has tried to find the next shot too many times, raise an error
                    print("Bot is stuck in hunt mode, taking random shot")
                    return self.random_shot(board)
                
        else:
            # If the hunt direction is not set, pick a random direction to start hunting
            # Keep trying until a valid direction is found
            while True:
                attempt += 1
                self.hunt_direction = random.randint(0, 3)
                if self.hunt_direction == 0:  # Up
                    shot_row = self.last_hit[0] - 1
                    shot_column = self.last_hit[1]
                elif self.hunt_direction == 1:  # Down
                    shot_row = self.last_hit[0] + 1
                    shot_column = self.last_hit[1]
                elif self.hunt_direction == 2:  # Left
                    shot_row = self.last_hit[0]
                    shot_column = self.last_hit[1] - 1
                elif self.hunt_direction == 3:  # Right
                    shot_row = self.last_hit[0]
                    shot_column = self.last_hit[1] + 1

                # Check if the shot is within bounds and not already shot at, if so return the coordinates
                if (0 <= shot_row < self.rows and
                    0 <= shot_column < self.columns and
                    not board[shot_row][shot_column]["is_shot"]):
                    # If the next shot is valid, update the last hit and return the coordinates
                    return (shot_row, shot_column)
                
                if attempt > 100: # If the bot has tried to find the next shot too many times, raise an error
                    print("Bot is stuck in hunt mode, taking random shot")
                    return self.random_shot(board)

    def bot_turn(self, board: List[List[dict]]) -> bool:
        """
        The bot's turn to make a shot on the game board.
        1. Decide where to shoot.
        2. Make shot and check if it hit a ship.
        3. If it hit a ship, check if it sunk the ship.
        4. If it sunk a ship, reset hunt mode.
        5. If it did not hit a ship, end turn.
        6. If it hit a ship, update the last hit and first hit coordinates.
        
        Args:
            board (List[List[dict]]): The game board where the bot will make a shot.
        
        Returns:
            bool: True if a ship was sunk, False otherwise. Used to check for end of game.
        """
        if self.hunt_mode_active:
            shot = self.hunt_mode(board)
        else:
            # If not in hunt mode, use the checkboard pattern for the first shots
            if len(self.checkboard_pattern) > 0:
                num = random.randint(0, len(self.checkboard_pattern) - 1)
                shot = self.checkboard_pattern.pop(num)  # Pop a random shot from the checkboard pattern
            elif len(self.adjactent_pattern) > 0:
                # If the checkboard pattern is empty, use the adjacent pattern
                num = random.randint(0, len(self.adjactent_pattern) - 1)
                shot = self.adjactent_pattern.pop(num) # Pop a random shot from the adjacent pattern
            else:
                # If both patterns are empty, resort to random shots on the board
                shot = self.random_shot(board)

        shot_hit: bool = False # Flag to indicate if the shot hit a ship
        ship_sunk: bool = False # Flag to indicate if a ship was sunk

        board[shot[0]][shot[1]]['is_shot'] = True  # Mark the tile as shot at
        if board[shot[0]][shot[1]]['is_occupied']:
            board[shot[0]][shot[1]]["ship"].hits += 1  # Increment the hit count of the ship
            shot_hit = True

            if board[shot[0]][shot[1]]["ship"].check_sunk():
                ship_sunk = True
        
        if not shot_hit: # If the shot missed, end turn
            self.last_shot_hit = False
            return
        
        if ship_sunk: # If the last shot sunk a ship, reset bot's hunt mode
            self.hunt_mode_active = False
            self.first_hit = None
            self.last_hit = None
            self.last_shot_hit = False
            self.hunt_direction = None
            return ship_sunk # End turn
        
        # If the first hit is not set, set it to the last hit
        if self.first_hit is None:
            self.first_hit = shot
            self.hunt_mode_active = True

        self.last_hit = shot  # Update the last hit to the current shot
        self.last_shot_hit = True  # Mark the last shot as a hit

        return ship_sunk # End turn              

    def random_shot(self, board: List[List[dict]]):
        # If both patterns are empty, resort to random shots on the board
        while True:
            shot_row = random.randint(0, self.rows - 1)
            shot_column = random.randint(0, self.columns - 1)
            if not board[shot_row][shot_column]["is_shot"]:
                shot = (shot_row, shot_column)
                return shot


if __name__ == "__main__":
    # Example usage
    bot = Bot(name="Bot1", rows=10, columns=10)
    print(f"Bot Name: {bot.name}")
    print(f"Checkboard Pattern Coordinates: {bot.checkboard_pattern}")
    print(f"Adjacent Pattern Coordinates: {bot.adjactent_pattern}")