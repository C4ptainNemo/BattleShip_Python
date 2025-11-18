""" Functions to create the game board and display it 

    Functions:
        create_board(row: int, column:int) -> List[List[dict]]:
            Create a game board with the specified number of rows and columns.
        
        display_board(board: List[List[dict]], own_board:bool) -> None:
            Display the game board in a readable format.    
"""

from typing import List
import ANSI
import gameFunctions

# Define the initial state of a cell in the game board
cell_state: dict = {
    "tile": "~", # Default tile representation, changed to ship tile when a ship is placed
    "is_occupied": False, # Flag to indicate if the cell is occupied by a ship
    "is_shot": False, # Flag to indicate if the cell has been shot at
    "ship": None # Placeholder for ship object
    }

class gameBoard:
    """
    Class to represent the game board.
    
    Attributes:
        board (List[List[dict]]): A 2D list representing the game board, where each cell is a dictionary.
    """
    
    def __init__(self, row: int, column: int):
        """
        Initialize the game board with the specified number of rows and columns.
        
        Args:
            row (int): Number of rows in the board.
            column (int): Number of columns in the board.
        """
        self.column_headers:str = None # Pregenerated column headers, eg. 1 2 3 4. Compute this once at board creation then just print the string
        self.top_bottom_border:str = None # Pregenerated top and bottom border of set length
        self.row_headers:list = [] # Pregenerated list of row headers, needs to be list so each row can index it.
        
        self.board = self.create_board(row, column) # Create the board

    def create_board(self, rows: int, columns:int) -> List[List[dict]]:
        """
        Create a game board with the specified number of rows and columns.
        Due to only spaceing filled tiles 1 apart this will not align correctly after column 999.
        
        Args:
            row (int): Number of rows in the board.
            column (int): Number of columns in the board.
        
        Returns:
            List[List[dict]]: A 2D list representing the game board, where each cell is a dictionary.
        """
        # Create a 2D list (board) with the specified number of rows and columns
        # Each cell is initialized with a copy of the cell_state dictionary
        board = [[cell_state.copy() for _ in range(columns)] for _ in range(rows)]

        # Generate row headers
        # Get the letter code for each row
        row_headers = [gameFunctions.int_to_letters(i) for i in range(rows)]
        # Get the length of the largest row header, which will be the last
        row_header_length = len(row_headers[-1])
        # Add padding to each header to make its length equal row_header_length + 1 and border #
        for i in range(len(row_headers)):
            length = len(row_headers[i]) # Get length of header
            row_headers[i] = row_headers[i] + (" " * (row_header_length - length + 1) + "# ")
        self.row_headers = row_headers

        # Generate column headers
        # At 10 there is no spacing between tiles
        # At 100 it doesn't align correctly
        column_headers = " " * (row_header_length + 3) # Add padding to align
        col_counter = 1
        while col_counter <= 9 and col_counter <= columns: # Add space before and after single digit
            column_headers += str(col_counter) + " "
            col_counter += 1
        while col_counter <= columns: # Add no space to triple digits
            column_headers += str(col_counter)
            col_counter += 1
        self.column_headers = column_headers

        # Generate top and bottom borders, add padding based on length of row headers and # based on number of columns
        self.top_bottom_border = " " * (row_header_length + 1) + "#" * (columns * 2 + 3)

        return board

    def display_board(self, own_board:bool) -> None:
        """
        Display the game board in a readable format.
        
        Args:
            own_board (bool): Flag to indicate if the board is the player's own board or the opponent's board.
        """
        rows = len(self.board[0])  # Number of rows in the board
        columns = len(self.board)  # Number of columns in the board

        # Print title
        title_length_factor = -5 if own_board else -11  # Adjust title length based on whether it's own board or opponent's board, number is (5 - number of characters in the title)
        padding = int((rows * 2 + title_length_factor) / 2)  # Will cause an error if rows is less than 2, but that will cause other issues
        print(" " * padding, end = "")  # Padding to center the title
        if own_board:
            print(ANSI.FG_BRIGHT_GREEN + "Your Board" + ANSI.RESET)
        else:
            print(ANSI.FG_BRIGHT_RED + "Opponent's Board" + ANSI.RESET)

        # Print column headers
        print(self.column_headers)
        # Print top border
        print(self.top_bottom_border)
        
        # Print game board
        for i in range(rows):
            # Print row header
            print(self.row_headers[i], end="")
            for j in range(columns):
                if own_board: # If players own board show the ship that is on the tile
                    tile = self.board[i][j]["tile"]
                else:
                    tile = "~" # Default tile for opponent's board
                
                if self.board[i][j]["is_shot"]: # If the cell has been shot at
                    if self.board[i][j]["is_occupied"]: # If the cell is occupied by a ship
                        print(ANSI.BG_RED + tile + ANSI.RESET + " ", end = "")
                    else: # If the cell is not occupied
                        print(ANSI.BG_WHITE + tile + ANSI.RESET + " ", end = "")
                else: # If the cell has not been shot at
                    print(tile + " ", end = "")
            print("#") 
        
        # Print bottom border
        print(self.top_bottom_border)  

    def clear_board(self) -> None:
        """
        Clear the game board by resetting all cells to their initial state.
        """
        for row in self.board:
            for cell in row:
                cell.update(cell_state)

if __name__ == "__main__":
    # Initialize colorama for cross-platform compatibility
    ANSI.colorama.init()
    
    # Create test boards with ships and shots
    player_board = gameBoard(10, 10)
    player_board.board[0][0]["tile"] = "B"
    player_board.board[0][0]["is_occupied"] = True
    player_board.board[1][0]["tile"] = "B"
    player_board.board[1][0]["is_occupied"] = True
    player_board.board[0][0]["is_shot"] = True
    player_board.board[1][1]["is_shot"] = True

    opponent_board = gameBoard(10, 10)
    opponent_board.board[0][0]["tile"] = "B"
    opponent_board.board[0][0]["is_occupied"] = True
    opponent_board.board[1][0]["tile"] = "B"
    opponent_board.board[1][0]["is_occupied"] = True
    opponent_board.board[0][0]["is_shot"] = True
    opponent_board.board[1][1]["is_shot"] = True 
   
    player_board.display_board(own_board=False)
    opponent_board.display_board(own_board=True)