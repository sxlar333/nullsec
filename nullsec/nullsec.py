from colorama import Fore, Style, init
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()
import os, time, sys
init(autoreset=True)

RED = "\033[31m"
GREEN = Fore.GREEN
YELLOW = Fore.GREEN
BLUE = Fore.BLUE
RESET = "\033[0m"
BRIGHT = Style.BRIGHT

modulesloaded = 0
version = "V1.0"
current_dir = os.getcwd()
username_pc = os.getlogin()

if sys.platform.startswith("win"):
    os_name = "Windows"
elif sys.platform.startswith("linux"):
    os_name = "Linux"
else:
    os_name = "Unknown"

def handle_cd(args):
    global current_dir

    if not args:
        print("Usage: cd <path>")
        return

    path = args[0]

    new_path = os.path.abspath(os.path.join(current_dir, path))

    if os.path.isdir(new_path):
        current_dir = new_path
        os.chdir(new_path) 
        print("Now in:", current_dir)
    else:
        print("No such directory:", path)

def handle_pwd(args):
    os.system("pwd")

def handle_clear(args):
    clear()
    show_banner()

def handle_exit(args):
    clear()
    sys.exit()

def handle_echo(args):
    print(" ".join(args))\

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def sutils():
    print(f"[{GREEN}+{RESET}] NullSec Initialized")
    sys.stdout.write(f"\x1b]2;nullsec | Modules active: {modulesloaded}\x07")

def banner():
    banner = r"""
     ███▄    █  █    ██  ██▓     ██▓      ██████ ▓█████  ▄████▄  
     ██ ▀█   █  ██  ▓██▒▓██▒    ▓██▒    ▒██    ▒ ▓█   ▀ ▒██▀ ▀█  
    ▓██  ▀█ ██▒▓██  ▒██░▒██░    ▒██░    ░ ▓██▄   ▒███   ▒▓█    ▄ 
    ▓██▒  ▐▌██▒▓▓█  ░██░▒██░    ▒██░      ▒   ██▒▒▓█  ▄ ▒▓▓▄ ▄██▒
    ▒██░   ▓██░▒▒█████▓ ░██████▒░██████▒▒██████▒▒░▒████▒▒ ▓███▀ ░
    ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░ ▒░▓  ░▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ░▒ ▒  ░
    ░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░ ▒  ░░ ░ ▒  ░░ ░▒  ░ ░ ░ ░  ░  ░  ▒   
       ░   ░ ░  ░░░ ░ ░   ░ ░     ░ ░   ░  ░  ░     ░   ░        
             ░    ░         ░  ░    ░  ░      ░     ░  ░░ ░      
                                                        ░        
    """
    colored_banner = Text(banner, style="bold red",)
    console.print(Align.center(colored_banner))
    
    info = Text.from_ansi(f"NullSec [{RED}{version}{RESET}]  [{RED}INFO{RESET}] Makes backdoors easy")
    console.print(
        Align.center(
            Panel.fit(info, border_style="bright_red")
        )
    )

def menu():
    menu_options = Text.from_ansi(f"""
    [{RED}echo{RESET}] echo
    [{RED}cd{RESET}] cd
    [{RED}pwd{RESET}] pwd
    [{RED}clear{RESET}] clear
    [{RED}e{RESET}/{RED}exit{RESET}] Exit
    """)
    console.print(Panel(menu_options, title="NullSec Menu", border_style="red"))

def show_banner():
    banner()
    menu()

def input_loop():
    commands = {
        "clear": handle_clear,
        "exit": handle_exit,
        "e": handle_exit,
        "echo": handle_echo,
        "cd": handle_cd,
        "pwd": handle_pwd,
    }
    while True:
        uin = input(f"""
{RED}┌──{RESET}({username_pc}{RED}@{RESET}{os_name}){RED}─{RESET}[~/NullSec {RED}{version}{RESET}]
{RED}│{RESET}                      
{RED}└─{RESET}$ """).lower()
        
        if not uin:
            continue
        
        parts = uin.split()
        cmd = parts[0]
        args = parts[1:]
        
        action = commands.get(cmd)
        
        if action:
            action(args)
        else:
            console.print(Text.from_ansi(f"[{RED}!{RESET}] Unknown Command: {uin}"))

def main():
    clear()
    banner()
    menu()
    input_loop()

if __name__ == "__main__":
    main()