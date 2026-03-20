from colorama import Fore, Style, init
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.GREEN
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

import os, socket

console = Console()
init(autoreset=True)

output_folder = "output/"

def build_menu():
    PORT = "change_this"
    IP = "change_this"
    banner = Text.from_ansi(rf"""
            \
            /                                 />           
            \__+_____________________/\/\___/ /|
            ()______________________      / /|/\
                         /0 0  ---- |----    /---\
                        |0 o 0 ----|| - \ --|      \
                         \0_0/____/ |    |  |\      \
                                     \__/__/  |      \
                                              |       \
                                              |         \
                                              |__________|
""")
    current_exploits_available = Text.from_ansi(f"""
    [{RED}RVSHELL{RESET}]: 1
    [{RED}RAT{RESET}]: 0









""")
    
    console.print(
        Columns(
            [
                Panel(
                    banner,
                    style="bold red",
                    border_style="bold red",
                    title="Exploit builder",
                ),
                Panel(
                    current_exploits_available,
                    border_style="bold red",
                    title="Exploits Available",
                ),
            ],
            expand=True,
        )
    )
    
    menu_view = Text.from_ansi(f"""
    [{RED}PORT{RESET}] {PORT}
    [{RED}IP{RESET}] {IP}
    
""")
    console.print(
        Panel(menu_view, border_style="bold red", title="Settings")
    )


build_menu()