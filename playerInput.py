""" Functions to handle player input for the game 

    Functions:
        player_input_confirm(prompt: str) -> bool:
            Confirm the player's input with a yes/no question.
        
        player_input_coord(rows: int, columns: int) -> tuple:
            Get the player's input for coordinates in the format row(str)column(int).
        
        player_input_direction() -> str:
            Get the player's input for direction.
        
        player_input_int(prompt: str, min_value: int, max_value: int) -> int:
            Get a number input from the player within a specified range.
"""
import ANSI


def player_input_confirm(prompt:str) -> bool:
    """
    Confirm the player's input with a yes/no question.
    
    Args:
        prompt (str): The question to ask the player.
    
    Returns:
        bool: True if the player confirms, False otherwise.
    """
    while True:
        response = input(prompt + " (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'")

def player_input_coord(board_rows:int, board_columns: int) -> tuple:
    """
    Get the player's input for coordinates. Input will be in the format row:str column:int
    Currently limits size of the board to 26 rows (A-Z)

    Args:
        board_rows (int): The number of rows in the game board.
        board_columns (int): The number of columns in the game board.
    
    Returns:
        tuple: A tuple containing the row and column indices (0-indexed).
    """
    prompt = f"Enter coordinates - A 1 to {chr(board_rows+64)} {board_columns}: "
    while True:
        try:
            input_str = input(prompt).upper().split(sep = " ")
            if len(input_str) != 2:
                raise ValueError("Invalid Coordinate: Please enter coordinate in the format 'Row Column' (e.g., A 1)")
            
            row_input = ord(input_str[0]) - 65  # Subtract 65 to convert ASCII to index, convert to 0-indexed
            column_input = int(input_str[1]) - 1  # Convert to 0-indexed
            
            if row_input < 0 or row_input >= board_rows or column_input < 0 or column_input >= board_columns:
                raise ValueError(f"Coordinates out of bounds - A 1 to {chr(board_rows+64)} {board_columns}")
            
            return (row_input, column_input)
        
        except ValueError as e:
            print(f"{e}: ")

def player_input_direction() -> str:
    """
    Get the player's input for direction and convert to integer values.
    
    Returns:
        str: The direction input by the player ("up", "down", "left", "right").
    """
    while True:
        direction = input("Enter direction - up (u), down (d), left (l), right (r): ").strip().lower()
        if direction in ["up", "u"]:
            return "up"
        if direction in ["down", "d"]:
            return "down"
        if direction in ["left", "l"]:
            return "left"
        if direction in ["right", "r"]:
            return "right"
        else:
            print("Invalid direction")

def player_input_int(prompt:str, min_value:int, max_value:int) -> int:
    """
    Get a integer input from the player within a specified range.
    
    Args:
        prompt (str): The prompt to display to the player.
        min_value (int): The minimum acceptable value.
        max_value (int): The maximum acceptable value.
    
    Returns:
        int: The number input by the player.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a number between {min_value} and {max_value}")
        except ValueError:
            print("Invalid input. Please enter a valid number")

def player_input_float(prompt:str, min_value:float, max_value:float) -> float:
    """
    Get a float input from the player within a specified range.
    
    Args:
        prompt (float): The prompt to display to the player.
        max_value (float): The maximum acceptable value.
        min_value (float): The minimum acceptable value.
        max_value (float): The maximum acceptable value.
    
    Returns:
        int: The float input by the player.
    """
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a number between {min_value} and {max_value}")
        except ValueError:
            print("Invalid input. Please enter a valid number")

def player_input_continue(prompt:str) -> None:
    """
    Asks the player to press enter to continue. This don't really do anything apart from wait until enter is pressed.
    """
    input(prompt)

if __name__ == "__main__":
    # Testing the player input functions
    rows = 10  # Example number of rows
    columns = 10  # Example number of columns
    
    loop = True
    while loop:
        coord = player_input_coord(rows, columns)
        print(f"Numerical Coord Value: {coord[0]},{coord[1]}")
        print(f"You entered coordinates: {chr(coord[0] + 65)} {coord[1] + 1}")

        direction = player_input_direction()
        print(f"Direction: {direction}")

        number = player_input_int("Enter a number between 1 and 10: ", 1, 10)
        print(f"You entered number: {number}")
        
        if player_input_confirm("Do you want to continue?"):
            print("Continuing the game...")
        else:
            print("Exiting the game...")
            loop = False