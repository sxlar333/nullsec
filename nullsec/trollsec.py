from colorama import Fore, Style, init
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from program.builder import build_menu, build, set_os_target

console = Console()
import os, sys, socket, base64, subprocess, time
import readline

init(autoreset=True)

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

version = "V2.5.6"
current_dir = os.getcwd()
username_pc = os.getlogin()

if sys.platform.startswith("win"):
    os_name = "Windows"
elif sys.platform.startswith("linux"):
    os_name = "Linux"
else:
    os_name = "Unknown"

# ─── Theme system ──────────────────────────────────────────────────────────────

THEMES = {
    "red": {
        "primary": Fore.RED,
        "accent": Fore.YELLOW,
        "rich": "bold red",
        "ansi": "\033[1;31m",
    },
    "green": {
        "primary": Fore.GREEN,
        "accent": Fore.CYAN,
        "rich": "bold green",
        "ansi": "\033[1;32m",
    },
    "cyan": {
        "primary": Fore.CYAN,
        "accent": Fore.GREEN,
        "rich": "bold cyan",
        "ansi": "\033[1;36m",
    },
    "blue": {
        "primary": Fore.BLUE,
        "accent": Fore.CYAN,
        "rich": "bold blue",
        "ansi": "\033[1;34m",
    },
    "yellow": {
        "primary": Fore.YELLOW,
        "accent": Fore.RED,
        "rich": "bold yellow",
        "ansi": "\033[1;33m",
    },
    "purple": {
        "primary": Fore.MAGENTA,
        "accent": Fore.CYAN,
        "rich": "bold magenta",
        "ansi": "\033[1;35m",
    },
}
THEME_FILE = ".trollsec_theme"


def load_theme():
    try:
        with open(THEME_FILE) as f:
            name = f.read().strip()
        if name in THEMES:
            return name
    except FileNotFoundError:
        pass
    return "red"


current_theme = load_theme()
RED = THEMES[current_theme]["primary"]
RICH_STYLE = THEMES[current_theme]["rich"]
ANSI_STYLE = THEMES[current_theme]["ansi"]

# ─── Changelog ─────────────────────────────────────────────────────────────────

CHANGELOG = [
    (
        "V2.0",
        [
            "Rework + Split",
            "10 troll scripts: BSOD, rickroll, fake virus, notifications,",
            "  screamer, desktop chaos, fake update, keyboard troll,",
            "  desktop flip, activate watermark",
            "Windows + Linux payload targets",
            "Typewriter banner effect",
            "Theme switcher",
            "Tab completion",
        ],
    ),
]

# ─── Handlers ─────────────────────────────────────────────────────────────────


def handle_help(args):
    help_text = Text.from_ansi(f"""
[{RED}Developer{RESET}]  sxlar/ez
[{RED}Version{RESET}]    {version}

[{RED}Navigation{RESET}]
  cd <path>       Change directory
  ls / dir        List directory
  pwd             Working directory
  open <file>     Print file contents
  clear           Clear screen
  echo <text>     Echo text
  e / exit        Exit TrollSec

[{RED}Builder{RESET}]
  scripts         Open troll script builder
  build           Quick build info
  --payload <os>  Set target OS (windows/linux)

[{RED}Encoding{RESET}]
  encode b64/hex <text>    Encode
  decode b64/hex <text>    Decode

[{RED}Network{RESET}]
  ping <host>     Ping a host

[{RED}Other{RESET}]
  help            Show this menu
""")
    console.print(Panel.fit(help_text, border_style=RICH_STYLE, title="TrollSec Help"))


def handle_ls(args):
    path = args[0] if args else "."
    try:
        for item in os.listdir(path):
            print(item)
    except FileNotFoundError:
        print(f"[{RED}!{RESET}] Directory not found")


def handle_open(args):
    if not args:
        print(f"[{RED}Usage{RESET}] open <file>")
        return
    try:
        with open(args[0], "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"[{RED}!{RESET}] File not found: {args[0]}")
    except PermissionError:
        print(f"[{RED}!{RESET}] Permission denied: {args[0]}")
    except UnicodeDecodeError:
        print(f"[{RED}!{RESET}] Cannot read binary file: {args[0]}")


def handle_cd(args):
    global current_dir
    if not args:
        print(f"[{RED}Usage{RESET}] cd <path>")
        return
    new_path = os.path.abspath(os.path.join(current_dir, args[0]))
    if os.path.isdir(new_path):
        current_dir = new_path
        os.chdir(new_path)
    else:
        print(f"No such directory: {args[0]}")


def handle_pwd(args):
    print(current_dir)


def handle_clear(args):
    clear()
    show_banner()


def handle_exit(args):
    clear()
    sys.exit()


def handle_echo(args):
    print(" ".join(args))


def handle_ping(args):
    if not args:
        print(f"[{RED}Usage{RESET}] ping <host>")
        return
    host = args[0]
    count = args[1] if len(args) > 1 else "4"
    print(f"[{GREEN}>{RESET}] Pinging {host}...")
    try:
        flag = "-n" if os.name == "nt" else "-c"
        result = subprocess.run(
            ["ping", flag, count, host], capture_output=True, text=True, timeout=15
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"[{RED}!{RESET}] Host unreachable or not found")
    except subprocess.TimeoutExpired:
        print(f"[{RED}!{RESET}] Ping timed out")


def handle_encode(args):
    if len(args) < 2:
        print(f"[{RED}Usage{RESET}] encode <b64|hex> <text>")
        return
    mode = args[0].lower()
    text = " ".join(args[1:])
    try:
        if mode == "b64":
            print(f"[{GREEN}>{RESET}] {base64.b64encode(text.encode()).decode()}")
        elif mode == "hex":
            print(f"[{GREEN}>{RESET}] {text.encode().hex()}")
        else:
            print(f"[{RED}!{RESET}] Unknown mode (use b64 or hex)")
    except Exception as e:
        print(f"[{RED}!{RESET}] Encode error: {e}")


def handle_decode(args):
    if len(args) < 2:
        print(f"[{RED}Usage{RESET}] decode <b64|hex> <text>")
        return
    mode = args[0].lower()
    text = " ".join(args[1:])
    try:
        if mode == "b64":
            print(f"[{GREEN}>{RESET}] {base64.b64decode(text.encode()).decode()}")
        elif mode == "hex":
            print(f"[{GREEN}>{RESET}] {bytes.fromhex(text).decode()}")
        else:
            print(f"[{RED}!{RESET}] Unknown mode (use b64 or hex)")
    except Exception as e:
        print(f"[{RED}!{RESET}] Decode error: {e}")


def handle_builder(args):
    build_menu()


def handle_build(args):
    build()


def handle_payload(args):
    if not args:
        print(f"[{RED}Usage{RESET}] --payload <windows|linux>")
        return
    set_os_target(args[0])


def handle_theme(args):
    global current_theme, RED, RICH_STYLE, ANSI_STYLE
    if not args:
        print(f"\n  Current theme: {current_theme}")
        print(f"  Available:     {', '.join(THEMES.keys())}\n")
        return
    name = args[0].lower()
    if name not in THEMES:
        print(f"[{RED}!{RESET}] Unknown theme. Choose from: {', '.join(THEMES.keys())}")
        return
    current_theme = name
    RED = THEMES[name]["primary"]
    RICH_STYLE = THEMES[name]["rich"]
    ANSI_STYLE = THEMES[name]["ansi"]
    globals()["RED"] = RED
    globals()["RICH_STYLE"] = RICH_STYLE
    globals()["ANSI_STYLE"] = ANSI_STYLE
    with open(THEME_FILE, "w") as f:
        f.write(name)
    print(f"[{GREEN}+{RESET}] Theme set to: {name}")


def handle_changelog(args):
    text = Text.from_ansi(f"\n[{RED}Version History{RESET}]\n")
    for ver, changes in reversed(CHANGELOG):
        text.append(f"\n  {ver}\n", style="bold")
        for c in changes:
            text.append(f"    • {c}\n")
    console.print(Panel.fit(text, border_style=RICH_STYLE, title="Changelog"))


def handle_back(args):
    clear()
    raise SystemExit("__back__")


# ─── Core ──────────────────────────────────────────────────────────────────────


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def sutils():
    sys.stdout.write(f"\x1b]2;TrollSec {version}\x07")


def slow_print(text, delay=0.045):
    reset = "\033[0m"
    width = os.get_terminal_size().columns
    for line in text.splitlines():
        pad = max(0, (width - len(line)) // 2)
        sys.stdout.write(" " * pad + ANSI_STYLE + line + reset + "\n")
        sys.stdout.flush()
        time.sleep(delay)


def banner():
    logo = r"""
    ████████╗██████╗  ██████╗ ██╗     ██╗      ███████╗███████╗ ██████╗
       ██╔══╝██╔══██╗██╔═══██╗██║     ██║      ██╔════╝██╔════╝██╔════╝
       ██║   ██████╔╝██║   ██║██║     ██║      ███████╗█████╗  ██║     
       ██║   ██╔══██╗██║   ██║██║     ██║      ╚════██║██╔══╝  ██║     
       ██║   ██║  ██║╚██████╔╝███████╗███████╗ ███████║███████╗╚██████╗
       ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝ ╚══════╝╚══════╝ ╚═════╝
    """
    links = Text.from_ansi(
        f"[{RED}GITHUB{RESET}] https://github.com/sxlar333/nullsec  "
        f"[{RED}DISCORD{RESET}] https://discord.gg/dwte3mus4W"
    )
    console.print(
        Align.center(Panel.fit(links, border_style=RICH_STYLE, title="Links"))
    )
    slow_print(logo)
    info = Text.from_ansi(
        f"TrollSec [{RED}{version}{RESET}]  [{RED}INFO{RESET}] Prank Script Builder  "
        f"[{RED}SCRIPTS{RESET}] 10"
    )
    console.print(Align.center(Panel.fit(info, border_style=RICH_STYLE)))


def menu():
    menu_options = Text.from_ansi(f"""
  [{RED}Builder{RESET}]    scripts  --payload windows/linux
  [{RED}Encoding{RESET}]   encode  decode  (b64/hex)
  [{RED}Network{RESET}]    ping
  [{RED}Files{RESET}]      ls  cd  pwd  open  echo  clear
  [{RED}Other{RESET}]      theme  changelog  back  help  exit
    """)
    console.print(
        Panel(menu_options, title="TrollSec Commands", border_style=RICH_STYLE)
    )


def show_banner():
    banner()
    menu()


def input_loop():
    commands = {
        "clear": handle_clear,
        "c": handle_clear,
        "cls": handle_clear,
        "exit": handle_exit,
        "e": handle_exit,
        "echo": handle_echo,
        "cd": handle_cd,
        "pwd": handle_pwd,
        "help": handle_help,
        "open": handle_open,
        "ls": handle_ls,
        "dir": handle_ls,
        "ping": handle_ping,
        "encode": handle_encode,
        "decode": handle_decode,
        "scripts": handle_builder,
        "build": handle_build,
        "--payload": handle_payload,
        "theme": handle_theme,
        "changelog": handle_changelog,
        "back": handle_back,
    }

    def completer(text, state):
        options = [c for c in commands if c.startswith(text)]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        uin = input(f"""
{RED}┌──{RESET}({username_pc}{RED}@{RESET}{os_name}){RED}─{RESET}[~/{RED}Troll{RESET}Sec {RED}{version}{RESET}]
{RED}│{RESET}
{RED}└─{RESET}$ """)

        if not uin.strip():
            continue

        parts = uin.split()
        cmd = parts[0].lower()
        args = parts[1:]

        action = commands.get(cmd)
        if action:
            action(args)
        else:
            console.print(
                Text.from_ansi(f"[{RED}!{RESET}] Unknown command: {cmd} — type help")
            )


def main():
    clear()
    banner()
    menu()
    sutils()
    try:
        input_loop()
    except SystemExit as e:
        if str(e) == "__back__":
            import launcher

            launcher.main()
        else:
            sys.exit()


if __name__ == "__main__":
    main()
