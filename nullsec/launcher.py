from colorama import Fore, Style, init
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from nullsec import main as nullsec_main
from trollsec import main as trollsec_main
import sys, os, time

console = Console()
init(autoreset=True)

RED   = Fore.RED
GREEN = Fore.GREEN
RESET = Style.RESET_ALL

def slow_print(text, delay=0.045, style="\033[1;31m"):
    reset  = "\033[0m"
    width  = os.get_terminal_size().columns
    for line in text.splitlines():
        pad = max(0, (width - len(line)) // 2)
        sys.stdout.write(" " * pad + style + line + reset + "\n")
        sys.stdout.flush()
        time.sleep(delay)

def main():
    os.system("clear" if os.name != "nt" else "cls")

    logo = r"""
     ███▄    █  █    ██  ██▓     ██▓      ██████ ▓█████  ▄████▄  
     ██ ▀█   █  ██  ▓██▒▓██▒    ▓██▒    ▒██    ▒ ▓█   ▀ ▒██▀ ▀█  
    ▓██  ▀█ ██▒▓██  ▒██░▒██░    ▒██░    ░ ▓██▄   ▒███   ▒▓█    ▄ 
    ▓██▒  ▐▌██▒▓▓█  ░██░▒██░    ▒██░      ▒   ██▒▒▓█  ▄ ▒▓▓▄ ▄██▒
    ▒██░   ▓██░▒▒█████▓ ░██████▒░██████▒▒██████▒▒░▒████▒▒ ▓███▀ ░
    ░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ░ ▒░▓  ░░ ▒░▓  ░▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ░▒ ▒  ░
    ░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░ ▒  ░░ ░ ▒  ░░ ░▒  ░ ░ ░ ░  ░  ░  ▒   
       ░   ░ ░  ░░░ ░ ░   ░ ░     ░ ░   ░  ░  ░     ░   ░        
             ░    ░         ░  ░    ░  ░      ░     ░  ░░ ░      
    """

    slow_print(logo)

    mode_text = Text.from_ansi(f"""
  [{RED}1{RESET}] NullSec   —  Recon & CTF toolkit
  [{RED}2{RESET}] TrollSec  —  Prank script builder
  [{RED}q{RESET}] Quit
""")
    console.print(Align.center(Panel.fit(mode_text, border_style="bold red", title="Select Mode")))

    while True:
        choice = input(f"\n[{RED}>{RESET}] ").strip().lower()

        if choice == "1":
            nullsec_main()
            break
        elif choice == "2":
            trollsec_main()
            break
        elif choice in ("q", "quit", "exit"):
            os.system("clear" if os.name != "nt" else "cls")
            sys.exit()
        else:
            print(f"[{RED}!{RESET}] Enter 1, 2, or q")

if __name__ == "__main__":
    main()