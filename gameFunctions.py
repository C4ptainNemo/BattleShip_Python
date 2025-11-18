"""
Miscillanious functions for the game
"""
import os

def clear_console():
    """Clears the console screen"""
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def int_to_letters(number:int) -> str:
    """
    Converts an integer in base 26 and converts each positional value to letter, eg 0=A, 25=Z, 26=AA, 701=ZZ, 702=AAA
    The string is of length n + 1 where the number >= 26^n + 26^n-1 + 26^n-2 ... + 26^1 where n > 1.
    For number
    eg. AA = 26 = 26^1
    eg. AAA = 702 = 26^2 + 26^1
    eg. AAAA = 18278 = 26^3 + 26^2 + 26^1
    eg. AAAAA = 475252 = 26^4 + 26^3 + 26^2 + 26^1

    Args:
        number (int): The integer to be converted

    Returns:
        str: string of the letter code
    """
    # Check to ensure the number in of type int
    if not isinstance(number, int):
        raise TypeError("Can only accept integers")
    number = abs(number) # Make positive if not already
    num_list = []
    # Convert to base 26, working from least significant digit to most significant.
    while number >= 26:
        # Take the (number mod base) to get the positional value
        num_list.append(int(number % 26))
        # Then divide by the base, and subtract 1 to account for the ordinal starting at 0 and not 1
        number = int(number / 26) - 1
    # This deals with the most significant digit as the number > 26
    num_list.append(int(number % 26))
    # Reverse since it went from least to most significant
    num_list.reverse()
    # Convert each number to the appropriate charater, this is why 65 is added
    num_list = [chr(num + 65) for num in num_list]
    string = ""
    string = string.join(num_list)
    return string

if __name__ == "__main__":
    clear_console()

    print(int_to_letters(0))
    print(int_to_letters(1))
    print(int_to_letters(25))
    print(int_to_letters(26))
    print(int_to_letters(701))
    print(int_to_letters(702))
    print(int_to_letters(18277))
    print(int_to_letters(18278))
    print(int_to_letters(475253))
    print(int_to_letters(475254))