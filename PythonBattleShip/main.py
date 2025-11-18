""" 
Main entry point for the game. Contains the splash screen, front memu and settings.

Requires installation of colorama for cross-platform ANSI color support. -m pip install colorama
"""
# Imports
import ANSI
import gameModes
import gameFunctions
import playerInput

# Global Settings
debug_mode:bool = False
default_board_rows:int = 10
default_board_columns:int = 10

def main():
    # Initialize colorama for cross-platform compatibility
    ANSI.colorama.init()

    splash_screen()

    while True:
        gameFunctions.clear_console()
        print(ANSI.FG_BRIGHT_CYAN + "Welcome to Battleship!" + ANSI.RESET)
        print("Select a game mode:")
        print("1. Player vs Player")
        print("2. Player vs Computer")
        print("3. Computer Solo")
        print("4. Settings")
        print("5. Exit")

        choice = playerInput.player_input_int("Enter your choice (1-5): ", 1, 5)

        if choice == 1: # Player vs. Player
            gamemode_1()
        elif choice == 2: # Player vs. Computer
            gamemode_2()
        elif choice == 3: # Computer Solo
            gamemode_3()
        elif choice == 4: # Setting Menu
            settings_menu()
        elif choice == 5: # Exit game
            break
        else:
            print("Invalid choice, please try again.")

    print("\nThank you for playing! Goodbye!")

def splash_screen():
    """
    Splash screen for when the game opens
    """
    gameFunctions.clear_console()
    print("\t\t\t\t" + ANSI.FG_BRIGHT_CYAN + "Welcome to Battleship!" + ANSI.RESET)
    print("""
        
                                        |__
                                        |\/
                                        ---
                                        / | [
                                !      | |||
                                _/|     _/|-++'
                            +  +--|    |--|--|_ |-
                        { /|__|  |/\__|  |--- |||__/
                        +---------------___[}-_===_.'____                 
                    ____`-' ||___-{]_| _[}-  |     |_[___\==--                __
    __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
    |                                                                     BB-61/
    \_________________________________________________________________________|
    Matthew Bace
        
    """)
    playerInput.player_input_continue("\t\t\t\t" + ANSI.FG_BRIGHT_GREEN + "Press enter to continue" + ANSI.RESET)

def settings_menu():
    """
    Displays the settings menu and allows the user to change game settings.

        Settings:   Debug Mode
                    Board Size
    """
    while True:
        gameFunctions.clear_console()
        global debug_mode
        global default_board_rows
        global default_board_columns
        print(ANSI.FG_BRIGHT_CYAN + "Settings Menu" + ANSI.RESET)
        print(f"1. Debug Mode: {'On' if debug_mode else 'Off'}")
        print(f"2. Board Size: Rows = {default_board_rows}, Columns = {default_board_columns}")
        print("3. Back")
        choice = playerInput.player_input_int("Enter your choice (1-2): ", 1, 3)

        if choice == 1: # Set debug mode
            debug_mode = playerInput.player_input_confirm("Debug Mode On?")

        elif choice == 2: # Set board size
            print("Set Default Board Size")
            default_board_rows = playerInput.player_input_int("Number of Rows? (1-1000): ", 1, 1000)
            default_board_columns = playerInput.player_input_int("Number of Columns? (1-1000): ", 1, 1000)

        elif choice == 3: # Back
            break

# Player vs. Player
def gamemode_1():
    gameFunctions.clear_console()
    gameModes.player_vs_player()
    playerInput.player_input_continue(ANSI.FG_BRIGHT_GREEN + "Press enter to return to main menu" + ANSI.RESET)

# Player vs. Computer
def gamemode_2():
    # Options to set
    rows = default_board_rows
    columns = default_board_columns
    turn_time:float = 1 # How long the bot sleeps for between turns

    while True:
        gameFunctions.clear_console()
        print(ANSI.FG_BRIGHT_CYAN + "Player vs. Computer" + ANSI.RESET)
        print("Set game options")
        print(f"1. Board dimensions: {rows, columns}")
        print(f"2. Computer Turn Time: {turn_time} seconds")
        print(f"3. Start game")
        print(f"4. Back")

        choice = playerInput.player_input_int("Enter your choice (1-4): ", 1, 4)

        if choice == 1: # Set board size
            print("Set Board Size")
            rows = playerInput.player_input_int("Number of Rows? (1-64): ", 1, 64)
            columns = playerInput.player_input_int("Number of Columns? (1-64): ", 1, 64)
        elif choice == 2: # Turn time
            turn_time = playerInput.player_input_float("How long is the computers turn in seconds? (0.0-10.0): ", 0, 10.0)
        elif choice == 3: # Start game
            break
        elif choice == 4: # Back
            return

    gameModes.player_vs_computer(board_rows=rows, board_columns=columns, bot_turn_time=turn_time, debug_mode=debug_mode)
    playerInput.player_input_continue(ANSI.FG_BRIGHT_GREEN + "Press enter to return to main menu" + ANSI.RESET)

# Computer Solo
def gamemode_3():
    # Options to set
    rows = default_board_rows
    columns = default_board_columns
    games:int = 1 # Max number of games the bot will play
    show_turn:bool = True # Show every turn the bot makes
    show_end:bool = True # Show the winning game board, this allows only showing the end and not every turn
    turn_time:float = 0.1 # How long the bot sleeps for between turns
    clear_screen:bool = True # Clear the screen between turns, can turn off to look back at previous turns
    
    while True:
        gameFunctions.clear_console()
        print(ANSI.FG_BRIGHT_CYAN + "Computer Solo" + ANSI.RESET)
        print("This game mode allows you to observe the computer playing by itself\n")
        print("Set game options")
        print(f"1. Number of games: {games}")
        print(f"2. Board dimesnions: {rows, columns}")
        print(f"3. Shows every turn: {show_turn}")
        print(f"4. Show final turn: {show_end}")
        print(f"5. Clear screen between turns: {clear_screen}")
        print(f"6. Turn time: {turn_time} seconds")
        print(f"7. Start game")
        print(f"8. Back")

        choice = playerInput.player_input_int("Enter your choice (1-8): ", 1, 8)

        if choice == 1: # Numbers of games
            games = playerInput.player_input_int("How many games will the computer play? (0-999999): ", 0, 999999)
        elif choice == 2: # Set board size
            print("Set Board Size")
            rows = playerInput.player_input_int("Number of Rows? (1-1000): ", 1, 1000)
            columns = playerInput.player_input_int("Number of Columns? (1-1000): ", 1, 1000)
        elif choice == 3: # Show turns
            show_turn = playerInput.player_input_confirm("Show every turn the computer plays?")
        elif choice == 4: # Show end
            show_end = playerInput.player_input_confirm("Show the last turn? This allows only seeing the final turn")
        elif choice == 5: # Clear screen
            clear_screen = playerInput.player_input_confirm("Clear the console screen between turns?")
        elif choice == 6: # Turn time
            turn_time = playerInput.player_input_float("How long is the computers turn in seconds? (0.0-10.0): ", 0, 10.0)
        elif choice == 7: # Start game
            break
        elif choice == 8: # Back
            return

    gameModes.computer_solo(board_rows=rows, 
                            board_columns=columns, 
                            max_games=games, 
                            show_board_every_turn=show_turn, 
                            show_final_board=show_end, 
                            bot_slow_turn=True, 
                            bot_turn_time=turn_time,
                            clear_screen_bewteen_turns=clear_screen)
    print("Game Complete")
    playerInput.player_input_continue(ANSI.FG_BRIGHT_GREEN + "Press enter to return to main menu" + ANSI.RESET)

if __name__ == "__main__":
    main()