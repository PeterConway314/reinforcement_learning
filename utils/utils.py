import os

def clear_screen():
    # Clear command for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear command for Unix-like systems (Linux, macOS)
    else:
        os.system('clear')
