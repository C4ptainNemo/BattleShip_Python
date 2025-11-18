"""
ANSI Escape Codes

Ensure initialiseColorama() is called before any escape codes to enable cross-platform compatability.
"""

import colorama
from colorama import Fore, Back, Style

# Initialize colorama
def initialiseColorama():
    colorama.init()

# ANSI escape codes for foreground (text) colors
FG_BLACK          = Fore.BLACK
FG_RED            = Fore.RED
FG_GREEN          = Fore.GREEN
FG_YELLOW         = Fore.YELLOW
FG_BLUE           = Fore.BLUE
FG_MAGENTA        = Fore.MAGENTA
FG_CYAN           = Fore.CYAN
FG_WHITE          = Fore.WHITE

FG_BRIGHT_BLACK   = Fore.LIGHTBLACK_EX
FG_BRIGHT_RED     = Fore.LIGHTRED_EX
FG_BRIGHT_GREEN   = Fore.LIGHTGREEN_EX
FG_BRIGHT_YELLOW  = Fore.LIGHTYELLOW_EX
FG_BRIGHT_BLUE    = Fore.LIGHTBLUE_EX
FG_BRIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
FG_BRIGHT_CYAN    = Fore.LIGHTCYAN_EX
FG_BRIGHT_WHITE   = Fore.LIGHTWHITE_EX

# ANSI escape codes for background colors
BG_BLACK          = Back.BLACK
BG_RED            = Back.RED
BG_GREEN          = Back.GREEN
BG_YELLOW         = Back.YELLOW
BG_BLUE           = Back.BLUE
BG_MAGENTA        = Back.MAGENTA
BG_CYAN           = Back.CYAN
BG_WHITE          = Back.WHITE

BG_BRIGHT_BLACK   = Back.LIGHTBLACK_EX
BG_BRIGHT_RED     = Back.LIGHTRED_EX
BG_BRIGHT_GREEN   = Back.LIGHTGREEN_EX
BG_BRIGHT_YELLOW  = Back.LIGHTYELLOW_EX
BG_BRIGHT_BLUE    = Back.LIGHTBLUE_EX
BG_BRIGHT_MAGENTA = Back.LIGHTMAGENTA_EX
BG_BRIGHT_CYAN    = Back.LIGHTCYAN_EX
BG_BRIGHT_WHITE   = Back.LIGHTWHITE_EX

# ANSI escape codes for text styles
RESET             = Style.RESET_ALL
TXT_BOLD          = Style.BRIGHT
TXT_DIM           = Style.DIM



# # ANSI escape codes for foreground (text) colors
# FG_BLACK          = "\033[30m"  # Black
# FG_RED            = "\033[31m"  # Red
# FG_GREEN          = "\033[32m"  # Green
# FG_YELLOW         = "\033[33m"  # Yellow
# FG_BLUE           = "\033[34m"  # Blue
# FG_MAGENTA        = "\033[35m"  # Magenta
# FG_CYAN           = "\033[36m"  # Cyan
# FG_WHITE          = "\033[37m"  # White

# # ANSI escape codes for bright foreground (text) colors
# FG_BRIGHT_BLACK   = "\033[90m"  # Bright Black
# FG_BRIGHT_RED     = "\033[91m"  # Bright Red
# FG_BRIGHT_GREEN   = "\033[92m"  # Bright Green
# FG_BRIGHT_YELLOW  = "\033[93m"  # Bright Yellow
# FG_BRIGHT_BLUE    = "\033[94m"  # Bright Blue
# FG_BRIGHT_MAGENTA = "\033[95m"  # Bright Magenta
# FG_BRIGHT_CYAN    = "\033[96m"  # Bright Cyan
# FG_BRIGHT_WHITE   = "\033[97m"  # Bright White

# # ANSI escape codes for background colors
# BG_BLACK          = "\033[40m"  # Background Black
# BG_RED            = "\033[41m"  # Background Red
# BG_GREEN          = "\033[42m"  # Background Green
# BG_YELLOW         = "\033[43m"  # Background Yellow
# BG_BLUE           = "\033[44m"  # Background Blue
# BG_MAGENTA        = "\033[45m"  # Background Magenta
# BG_CYAN           = "\033[46m"  # Background Cyan
# BG_WHITE          = "\033[47m"  # Background White

# # ANSI escape codes for bright background colors
# BG_BRIGHT_BLACK   = "\033[100m" # Bright Background Black
# BG_BRIGHT_RED     = "\033[101m" # Bright Background Red
# BG_BRIGHT_GREEN   = "\033[102m" # Bright Background Green
# BG_BRIGHT_YELLOW  = "\033[103m" # Bright Background Yellow
# BG_BRIGHT_BLUE    = "\033[104m" # Bright Background Blue
# BG_BRIGHT_MAGENTA = "\033[105m" # Bright Background Magenta
# BG_BRIGHT_CYAN    = "\033[106m" # Bright Background Cyan
# BG_BRIGHT_WHITE   = "\033[107m" # Bright Background White

# # ANSI escape codes for text styles
# RESET             = "\033[0m"
# TXT_BOLD          = "\033[1m"   # Bold
# TXT_DIM           = "\033[2m"   # Dim
# TXT_ITALIC        = "\033[3m"   # Italic
# TXT_UNDERLINE     = "\033[4m"   # Underline
# TXT_BLINK         = "\033[5m"   # Blink
# TXT_INVERSE       = "\033[7m"   # Inverse
# TXT_HIDDEN        = "\033[8m"   # Hidden
# TXT_STRIKETHROUGH = "\033[9m"   # Strikethrough