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

import os

console = Console()
init(autoreset=True)

output_folder = "output/"
PORT = "change this"
IP = "change this"
OS = "default/linux"

def build_menu():
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
    current_scripts_available = Text.from_ansi(f"""
    [{RED}SHELL{RESET}]: 1










""")
    
    console.print(
        Columns(
            [
                Panel(
                    banner,
                    style="bold red",
                    border_style="bold red",
                    title="Script builder",
                ),
                Panel(
                    current_scripts_available,
                    border_style="bold red",
                    title="Scripts Available",
                ),
            ],
            expand=True,
        )
    )
    
    menu_view = Text.from_ansi(f"""
    [{RED}PORT{RESET}] {PORT}           [{RED}OS{RESET}] {OS}
    [{RED}IP{RESET}] {IP}               [{RED}?{RESET}]
    
""")
    console.print(
        Panel(menu_view, border_style="bold red", title="Settings")
    )

def port():
    global PORT
    PORT = input(f"[{RED}PORT{RESET}] {RED}>{RESET} ")

def ip():
    global IP
    IP = input(f"[{RED}IP{RESET}] {RED}>{RESET} ")

def os():
    global OS 
    OS = input(f"[{RED}OS{RESET}] {RED}>{RESET} ")

# maybe add functionality for os specific exploits? --deltadude
def build():
    output = f"""\
#in progress
#old script wasnt really good

"""
    os.makedirs("output", exist_ok=True)
    with open("output/rvshell.py", "w") as f:
        f.write(output)
        print(f"[{GREEN}+{RESET}] Succesfully generated rvshell")