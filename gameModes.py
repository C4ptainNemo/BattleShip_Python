""" Functins for running different game modes in a Battleship game.

    Functions:
        player_vs_player(player1: Player, player2: Player) -> None:
            Handle the game logic for player vs player mode.

        player_vs_computer(player: Player, computer: Computer) -> None:
            Handle the game logic for player vs player and player vs computer modes.

        computer_solo(player: Player) -> None:
            Handle the game logic for a solo computer game.
"""
import gameBoard
import gameFunctions
import playerInput
import ANSI
from ship import Ship
from bot import Bot
from time import sleep, time
from copy import deepcopy


def player_vs_player():
    """
    Handle the game logic for player vs player mode.
    """
    print("Starting Player vs Player mode...")
    print("Not yet implemented.")
    return

def player_vs_computer(board_rows:int, board_columns:int, bot_turn_time:float=1.0, debug_mode=False):
    """
    Handle the game logic for player vs computer mode.

    Args:
        board_rows (int): Number of rows on the game board.
        board_columns (int): Number of columns on the game board.
        bot_turn_time (float): How long the bot sleeps for between turns.
    """
    # Ships
    frigate = Ship("Frigate", "F", 2)
    destroyer = Ship("Destroyer", "D", 3)
    battleship = Ship("Battleship", "B", 4)
    carrier = Ship("Carrier", "C", 5)
    ship_list = [frigate, destroyer, battleship, carrier]

    # Bot setup
    bot_board = gameBoard.gameBoard(board_rows, board_columns)
    bot = Bot("Computer", board_rows, board_columns)
    bot_ship_list = deepcopy(ship_list)
    for ship in bot_ship_list:
        ship.random_place(bot_board.board, board_rows, board_columns)

    # Player setup
    player_board = gameBoard.gameBoard(board_rows, board_columns)
    player_ship_list = deepcopy(ship_list)

    # Have player place ships
    message = "" # Message to indicate certain things to player, such as ship couldn't be placed
    while True:
        # Set to none after exiting placement menu
        gameFunctions.clear_console()
        player_board.display_board(own_board=True)
        print(message)
        print("Ship\t\t\tBow Coordinate\t\tShip Direction\t\tOccupied Tiles")
        for i, ship in enumerate(player_ship_list):
            print(f"{i + 1}. {ship.name}\t\t{ship.bow_coord}\t\t\t{ship.direction}\t\t\t{ship.occupied_cells}")
        # Option to randomly place all ships
        print(f"{len(player_ship_list) + 1}. Randomly Place Ships")
        # Print option to start game after ships are shown
        print(f"{len(player_ship_list) + 2}. Start Game")
        # Select ship to place
        ship_choice = playerInput.player_input_int(f"Select Choice (1-{len(player_ship_list) + 1}): ", 1, len(player_ship_list) + 2)

        if ship_choice == len(player_ship_list) + 1: # Randomly place ships
            for ship in player_ship_list:
                ship.random_place(player_board.board, board_rows, board_columns)
            message = "All ships randomly placed"
            continue

        if ship_choice == len(player_ship_list) + 2: # Start game
            if all([ship.is_placed for ship in player_ship_list]):
                break
            else:
               message = "Not all ships are placed, cannot begin game"
               continue

        # Ship Placement menu
        ship_choice -= 1 # -1 to index list correctly
        message = "" # Reset message
        while True:
            gameFunctions.clear_console()
            player_board.display_board(own_board=True)
            print(message)
            print(f"{player_ship_list[ship_choice].name}\t\t{player_ship_list[ship_choice].bow_coord}\t\t\t{player_ship_list[ship_choice].direction}\t\t\t{player_ship_list[ship_choice].occupied_cells}")
            print(f"1. Place Ship")
            print(f"2. Reset Ship")
            print(f"3. Random Ship Placement")
            print(f"4. Back")

            place_choice = playerInput.player_input_int("Enter your choice (1-4): ", 1, 4)

            if place_choice == 1: # Place ship
                bow_coord = playerInput.player_input_coord(board_rows=board_rows, board_columns=board_columns)
                direction = playerInput.player_input_direction()
                if not player_ship_list[ship_choice].place(board=player_board.board, row=bow_coord[0], column=bow_coord[1], direction=direction, board_rows=board_rows, board_columns=board_columns):
                    message = "Ship could not be placed"

            elif place_choice == 2: # Reset ship
                player_ship_list[ship_choice].clear_ship(player_board.board)
            
            elif place_choice == 3: # Random placement
                player_ship_list[ship_choice].random_place(board=player_board.board, board_rows=board_rows, board_columns=board_columns)
            
            elif place_choice == 4: # Back
                break

        message = "" # Reset message

    # Play the game
    turn_counter = 0
    while True:
        turn_counter += 1

        # Debug mode
        if debug_mode:
            gameFunctions.clear_console()
            bot_board.display_board(own_board = True)
            player_board.display_board(own_board = True)
            print(ANSI.FG_BRIGHT_CYAN + "Debug Mode" + ANSI.RESET)
            print(f"1. Take turn")
            print(f"2. Sink own ships")
            print(f"3. Sink bots ships")

            choice = playerInput.player_input_int("Enter your choice (1-3): ", 1, 3)

            if choice == 1: # Take turn
                None
            elif choice == 2 or 3: # Sink all ships ships
                if choice == 2: 
                    ships = player_ship_list
                    board = player_board.board
                elif choice == 3: 
                    ships = bot_ship_list
                    board = bot_board.board
                for ship in ships:
                    for cell in ship.occupied_cells:
                        board[cell[0]][cell[1]]["is_shot"] = True
                        ship.hits += 1
                    ship.check_sunk()

        # Player Turn
        message = "" # Reset message
        while True:
            gameFunctions.clear_console()
            bot_board.display_board(own_board = False)
            player_board.display_board(own_board = True)
            print(ANSI.FG_BRIGHT_GREEN + "Your Turn" + ANSI.RESET)
            print(message)
            # Get a shot from the player
            player_shot = playerInput.player_input_coord(board_rows=board_rows, board_columns=board_columns)
            message = f"Your shot: {player_shot}"
            # Check if the cell is not yet shot
            if bot_board.board[player_shot[0]][player_shot[1]]["is_shot"]:
                message = "Cell has already been shot, try again"
                continue
            # If not shot then update board and check if ship was hit
            bot_board.board[player_shot[0]][player_shot[1]]['is_shot'] = True  # Mark the cell as shot at
            if bot_board.board[player_shot[0]][player_shot[1]]['is_occupied']:
                bot_board.board[player_shot[0]][player_shot[1]]["ship"].hits += 1  # Increment the hit count of the ship
                # If the ship is hit check if it is sunk, if so check all ships
                bot_board.board[player_shot[0]][player_shot[1]]["ship"].check_sunk()
            
            # Check if the ships are sunk
            sunk_counter = 0
            for ship in bot_ship_list:
                if ship.is_sunk:
                    sunk_counter += 1
            if sunk_counter >= len(bot_ship_list): # If all ships are sunk end the game
                gameFunctions.clear_console()
                bot_board.display_board(own_board=True) # Show the ship tiles once the game is over
                player_board.display_board(own_board=True)
                print(ANSI.BG_BRIGHT_GREEN + "Game Over: You sunk all the opponents ships" + ANSI.RESET)
                print(f"Turn Count: {turn_counter}")
                return
            # If a valid shot was made exit loop
            break

        # Computers Turn
        bot.bot_turn(player_board.board) # Bot takes turn, if ship is sunk will return true
        # Check of the players ships are sunk
        sunk_counter = 0
        for ship in player_ship_list: # If a ship gets sunk check if all ships are sunk
            if ship.is_sunk:
                sunk_counter += 1
        if sunk_counter >= len(player_ship_list):
            gameFunctions.clear_console()
            bot_board.display_board(own_board=True) # Show the ship tiles once the game is over
            player_board.display_board(own_board=True)
            print(ANSI.BG_BRIGHT_RED + "Game Over: Your opponent sunk all your ships" + ANSI.RESET)
            print(f"Turn Count: {turn_counter}")
            return

def computer_solo(board_rows:int, board_columns:int, max_games:int=1, show_board_every_turn:bool=True, show_final_board:bool=True, bot_slow_turn:bool=False, bot_turn_time:float=1.0, clear_screen_bewteen_turns:bool=False):
    """
    Handle the game logic for a solo computer game.

    Args:
        board_rows (int): Number of rows on the game board.
        board_columns (int): Number of columns on the game board.
        max_games (int): Number of games the bot will play.
        show_board_every_turn (bool): True to show display the board every turn.
        show_final_board (bool): True to show display the board at end of game.
        bot_slow_turn (bool): True to make the bot sleep between turns so it can be watched.
        bot_turn_time (float): How long the bot sleeps for between turns.
        clear_screen_between_turns (bool): True to clear the console sreen between turns.
    """
    game_number:int = 0
    total_score:int = 0
    
    while game_number < max_games:
        game_number += 1
        # Bot setup
        bot_board = gameBoard.gameBoard(board_rows, board_columns)
        bot = Bot("Computer", board_rows, board_columns)
        bot_turn_counter = 0

        # Ship setup
        frigate = Ship("Frigate", "F", 2)
        destroyer = Ship("Destroyer", "D", 3)
        battleship = Ship("Battleship", "B", 4)
        carrier = Ship("Carrier", "C", 5)
        ship_list = [frigate, destroyer, battleship, carrier]
        for ship in ship_list:
            ship.random_place(bot_board.board, board_rows, board_columns)
        
        # Show initial board
        if show_board_every_turn:
            if clear_screen_bewteen_turns:
                gameFunctions.clear_console()
            bot_board.display_board(own_board=True)
        if bot_slow_turn:
                sleep(bot_turn_time)

        while True:
            bot_turn_counter += 1
            if bot.bot_turn(bot_board.board): # Bot takes turn, if ship is sunk will return true
                sunk_counter = 0
                for ship in ship_list: # If a ship gets sunk check if all ships are sunk
                    if ship.is_sunk: # If any ship is not sunk break out of the loop
                        sunk_counter += 1
                if sunk_counter >= len(ship_list):
                    # If all ships are sunk end the game
                    if show_final_board:
                        if clear_screen_bewteen_turns:
                            gameFunctions.clear_console()
                        if bot_slow_turn:
                            sleep(bot_turn_time)
                        bot_board.display_board(own_board=True)
                    print(f"Game: {game_number}, Turns: {bot_turn_counter}")
                    break

            if show_board_every_turn:
                if clear_screen_bewteen_turns:
                    gameFunctions.clear_console()
                bot_board.display_board(own_board=True)
                if bot_slow_turn:
                    sleep(bot_turn_time)
        
        total_score += bot_turn_counter

    print("Game Over")
    print(f"Total Games: {max_games}")
    print(f"Average Score: {total_score / max_games}")

def bot_test():
    rows = 10
    columns = 10
    games = 1
    time_start = time()
    computer_solo(board_rows=rows, 
                  board_columns=columns, 
                  max_games=games, 
                  show_board_every_turn=True, 
                  show_final_board=True, 
                  bot_slow_turn=True, 
                  bot_turn_time=0.5,
                  clear_screen_bewteen_turns=False)
    time_end = time()
    print(f"Total Time: {time_end - time_start}")

def player_test():
    player_vs_computer(board_rows=10, board_columns=10, bot_turn_time=1.0, debug_mode=True)

if __name__ == "__main__":
    #player_test()
    bot_test()