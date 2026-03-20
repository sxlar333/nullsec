from colorama import Fore, Style, init
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from program.builder import build_menu, ip, port

console = Console()
import os, time, sys
init(autoreset=True)

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.GREEN
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

modulesloaded = 1
version = "V1.0"
current_dir = os.getcwd()
username_pc = os.getlogin()

if sys.platform.startswith("win"):
    os_name = "Windows"
elif sys.platform.startswith("linux"):
    os_name = "Linux"
else:
    os_name = "Unknown"

def handle_ip(args):
    ip()

def handle_port(args):
    port()

def handle_builder(args):
    build_menu()

def handle_help(args):
    help = Text.from_ansi(f"""
[{RED}Developer{RESET}] sxlar/ez
[{RED}Commands{RESET}] command --arg

""")
    console.print(
        Panel.fit(help, border_style="bold red", title="Help")
    )

def handle_ls(args):
    path = args[0] if args else "."
    
    try:
        for item in os.listdir(path):
            print(item)
    except FileNotFoundError:
        print(f"[{RED}!{RESET}] Directory not found")

def handle_open(args):
    filepath = args[0]
    with open(filepath, "r") as f:
        print(f.read())

def handle_cd(args):
    global current_dir

    if not args:
        print(f"[{RED}Usage{RESET}] cd <path>")
        return

    path = args[0]

    new_path = os.path.abspath(os.path.join(current_dir, path))

    if os.path.isdir(new_path):
        current_dir = new_path
        os.chdir(new_path) 
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
    sys.stdout.write(f"\x1b]2;nullsec | Modules active: {modulesloaded}\x07")

def banner():
    sxlar = Text.from_ansi(f"[{RED}GITHUB{RESET}] https://github.com/sxlar333/nullsec  [{RED}DISCORD{RESET}] https://discord.gg/dwte3mus4W")
    console.print(
        Align.center(
            Panel.fit(sxlar, border_style="bright_red", title="Links")
        )
    )

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
    
    info = Text.from_ansi(f"NullSec [{RED}{version}{RESET}]  [{RED}INFO{RESET}] Makes backdoors easy  [{RED}BACKDOORS{RESET}] 1")
    console.print(
        Align.center(
            Panel.fit(info, border_style="bright_red")
        )
    )

def menu():
    menu_options = Text.from_ansi(f"""
    [{RED}echo{RESET}] echo         [{RED}help{RESET}] help             [{RED}ip{RESET}] set ip
    [{RED}cd{RESET}] cd             [{RED}open{RESET}] open (file)      [{RED}?{RESET}]
    [{RED}pwd{RESET}] pwd           [{RED}ls/dir{RESET}] ls/dir         [{RED}?{RESET}]
    [{RED}clear{RESET}] clear       [{RED}exploits{RESET}] dashboard    [{RED}?{RESET}]
    [{RED}e{RESET}/{RED}exit{RESET}] Exit       [{RED}port{RESET}] set port         [{RED}?{RESET}]
    """)
    console.print(Panel(menu_options, title="NullSec Commands", border_style="red"))

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
        "help": handle_help,
        "open": handle_open,
        "ls": handle_ls,
        "dir": handle_ls,
        "exploit": handle_builder,
        "ip": handle_ip,
        "port": handle_port,
    }
    while True:
        uin = input(f"""
{RED}┌──{RESET}({username_pc}{RED}@{RESET}{os_name}){RED}─{RESET}[~/{RED}Null{RESET}Sec {RED}{version}{RESET}]
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
    sutils()
    input_loop()


if __name__ == "__main__":
    main()