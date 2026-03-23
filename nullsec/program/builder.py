from colorama import Fore, Style, init
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.columns import Columns
import os

console = Console()
init(autoreset=True)

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

output_folder = "output/"
OS_TARGET = "linux"  # default

SCRIPTS = {
    "1": "Fake BSOD / Error Screen",
    "2": "Rickroll",
    "3": "Fake Virus Scanner",
    "4": "Infinite Notifications",
    "5": "Screamer",
    "6": "Desktop Chaos",
    "7": "Fake Update Screen",
    "8": "Keyboard Troll",
    "9": "Desktop Flip",
    "10": "Activate Windows Watermark",
}

# ─── Payload templates ────────────────────────────────────────────────────────

def payload_fake_bsod(target_os):
    if target_os == "windows":
        return '''\
import tkinter as tk

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="#0078D7")
root.attributes("-topmost", True)

msg = """:(

Your PC ran into a problem that it couldn\'t handle, and now it needs to restart.

TROLL_DETECTED

If you\'d like to know more, you can search online later for this error:
FRIEND_GOT_REKT"""

label = tk.Label(root, text=msg, bg="#0078D7", fg="white",
                 font=("Segoe UI", 18), justify="left", anchor="nw")
label.pack(fill="both", expand=True, padx=80, pady=80)

btn = tk.Button(root, text="Click here to restart (jk)", bg="#0078D7", fg="white",
                font=("Segoe UI", 12), relief="flat", command=root.destroy)
btn.pack(pady=10)

root.mainloop()
'''
    else:
        return '''\
import tkinter as tk

root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.attributes("-topmost", True)

msg = """Kernel panic - not syncing: TROLL_DETECTED

CPU: 0 PID: 1337 Comm: init Tainted: G
Hardware name: Friend\'s PC
Call Trace:
  dump_stack+0x68/0x9a
  panic+0x101/0x2d4
  troll_activated+0x42/0x42
  ???

Rebooting in 10 seconds.. (not really lol)"""

label = tk.Label(root, text=msg, bg="black", fg="white",
                 font=("Courier", 14), justify="left", anchor="nw")
label.pack(fill="both", expand=True, padx=40, pady=40)

btn = tk.Button(root, text="ok fine you got me", bg="black", fg="white",
                font=("Courier", 11), relief="flat", command=root.destroy)
btn.pack(pady=10)

root.mainloop()
'''


def payload_rickroll(target_os):
    return '''\
import webbrowser, time

for _ in range(5):
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    time.sleep(0.5)

print("Never gonna give you up...")
'''


def payload_fake_virus(target_os):
    return '''\
import time, random

files = [
    "C:/Windows/System32/drivers/etc/hosts",
    "/etc/passwd", "/home/user/.ssh/id_rsa",
    "C:/Users/user/Documents/passwords.txt",
    "/var/log/auth.log", "C:/Windows/win.ini",
    "/etc/shadow", "C:/Users/user/Desktop/bank_details.xlsx",
    "/root/.bash_history", "C:/pagefile.sys",
]

threats = [
    "Trojan.GenericKD.48392", "Worm.AutoRun.GHJ",
    "Spyware.AgentTesla", "Ransomware.WannaCry.Variant",
    "Backdoor.Remcos.RAT", "Keylogger.Generic.XJ2",
]

print("\\n[NULLSEC ANTIVIRUS] Starting deep system scan...\\n")
time.sleep(1)

infected = 0
for f in files:
    time.sleep(random.uniform(0.3, 0.9))
    threat = random.choice(threats)
    infected += 1
    print(f"  [INFECTED] {f}")
    print(f"             \\u2514\\u2500 {threat}")

print(f"""
\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501
  SCAN COMPLETE
  Files scanned : {len(files)}
  Threats found : {infected}
  Status        : 100% INFECTED
\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501\\u2501

  You have been absolutely got lmao
""")
'''


def payload_notifications(target_os):
    if target_os == "windows":
        return '''\
from win10toast import ToastNotifier
import time, itertools

toaster = ToastNotifier()
messages = [
    "You have been got", "lmaooooo",
    "Did you check behind you?", "skill issue",
    "Your PC is fine btw", "gottem",
    "This will stop eventually", "or will it",
]

for msg in itertools.cycle(messages):
    toaster.show_toast("NullSec", msg, duration=2, threaded=True)
    time.sleep(2.5)
'''
    else:
        return '''\
import subprocess, time, itertools

messages = [
    "You have been got", "lmaooooo",
    "Did you check behind you?", "skill issue",
    "Your PC is fine btw", "gottem",
    "This will stop eventually", "or will it",
]

for msg in itertools.cycle(messages):
    subprocess.run(["notify-send", "NullSec", msg])
    time.sleep(2.5)
'''


def payload_screamer(target_os):
    return '''\
import time, tkinter as tk, threading, itertools

def flash():
    colors = ["red", "white", "black", "yellow"]
    for c in itertools.cycle(colors):
        root.configure(bg=c)
        time.sleep(0.05)

def play_sound():
    try:
        import winsound
        winsound.Beep(4000, 3000)
    except ImportError:
        import os
        os.system("play -n synth 3 sine 4000 2>/dev/null || beep 2>/dev/null || true")

print("Loading something cool...")
time.sleep(5)

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)

label = tk.Label(root, text="BOO!", font=("Arial Black", 120), fg="white")
label.pack(expand=True)

threading.Thread(target=flash, daemon=True).start()
threading.Thread(target=play_sound, daemon=True).start()

root.after(4000, root.destroy)
root.mainloop()
'''


def payload_desktop_chaos(target_os):
    if target_os == "windows":
        return '''\
import pyautogui, time, random, threading, os

pyautogui.FAILSAFE = False

def move_mouse():
    for _ in range(200):
        x = random.randint(0, pyautogui.size().width)
        y = random.randint(0, pyautogui.size().height)
        pyautogui.moveTo(x, y, duration=0.05)
        time.sleep(0.05)

def open_things():
    for _ in range(5):
        os.system("start notepad")
        time.sleep(0.5)

def spam_volume():
    time.sleep(2)
    for _ in range(30):
        pyautogui.press("volumeup")
        time.sleep(0.05)

threads = [
    threading.Thread(target=move_mouse),
    threading.Thread(target=open_things),
    threading.Thread(target=spam_volume),
]
for t in threads: t.start()
for t in threads: t.join()

print("chaos complete lol")
'''
    else:
        return '''\
import pyautogui, time, random, threading, subprocess

pyautogui.FAILSAFE = False

def move_mouse():
    w, h = pyautogui.size()
    for _ in range(200):
        pyautogui.moveTo(random.randint(0, w), random.randint(0, h), duration=0.05)
        time.sleep(0.05)

def open_things():
    for _ in range(5):
        subprocess.Popen(["xterm"])
        time.sleep(0.5)

threads = [
    threading.Thread(target=move_mouse),
    threading.Thread(target=open_things),
]
for t in threads: t.start()
for t in threads: t.join()

print("chaos complete lol")
'''


def payload_fake_update(target_os):
    return '''\
import tkinter as tk
import threading
import time

BG       = "#0a0a0a"
FG_WHITE = "#ffffff"
FG_DIM   = "#888888"
FG_BLUE  = "#0078d4"

STAGES = [
    "Getting things ready",
    "Checking for updates",
    "Downloading updates",
    "Installing updates",
    "Configuring your system",
    "Finishing up",
    "Almost done",
    "Your PC will restart shortly",
]

DOT_COUNT   = 5
DOT_SIZE    = 14
DOT_GAP     = 10
DOT_SPEED   = 120   # ms per frame
TRAIL       = 4     # how many dots glow behind the active one

def animate_dots(step=0):
    for i, dot_id in enumerate(dot_ids):
        # distance behind the active dot (wraps around)
        dist = (step - i) % DOT_COUNT
        if dist == 0:
            color = FG_BLUE
        elif dist <= TRAIL:
            # fade from blue to dark over the trail length
            fade = int(0x40 + (0x78 - 0x40) * (1 - dist / TRAIL))
            color = f"#00{fade:02x}d4"
        else:
            color = "#2a2a2a"
        dot_canvas.itemconfig(dot_id, fill=color)
    root.after(DOT_SPEED, animate_dots, (step + 1) % DOT_COUNT)

def advance_stage(idx=0):
    if idx < len(STAGES):
        status_var.set(STAGES[idx])
        root.after(2800, advance_stage, idx + 1)
    else:
        # reveal gottem screen
        root.after(1000, show_gottem)

def show_gottem():
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="black")
    tk.Label(root, text="lmaooo gottem", bg="black", fg="lime",
             font=("Segoe UI", 52, "bold")).pack(expand=True)
    tk.Label(root, text="there was no update.  you just sat there.",
             bg="black", fg="white", font=("Segoe UI", 18)).pack()
    tk.Button(root, text="ok fine", bg="black", fg="#888888",
              font=("Segoe UI", 13), relief="flat",
              command=root.destroy).pack(pady=24)

root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg=BG)

# ── Windows logo ─────────────────────────────────────────────────────────────
logo_canvas = tk.Canvas(root, width=64, height=64, bg=BG, highlightthickness=0)
logo_canvas.place(relx=0.5, rely=0.30, anchor="center")
logo_canvas.create_rectangle( 0,  0, 30, 30, fill="#f35325", outline="")
logo_canvas.create_rectangle(34,  0, 64, 30, fill="#81bc06", outline="")
logo_canvas.create_rectangle( 0, 34, 30, 64, fill="#05a6f0", outline="")
logo_canvas.create_rectangle(34, 34, 64, 64, fill="#ffba08", outline="")

# ── Heading ───────────────────────────────────────────────────────────────────
tk.Label(root, text="Working on updates", bg=BG, fg=FG_WHITE,
         font=("Segoe UI", 32, "bold")).place(relx=0.5, rely=0.40, anchor="center")

tk.Label(root, text="Don\'t turn off your PC. This will take a while.",
         bg=BG, fg=FG_DIM,
         font=("Segoe UI", 14)).place(relx=0.5, rely=0.47, anchor="center")

# ── Animated dots loader ──────────────────────────────────────────────────────
total_w = DOT_COUNT * DOT_SIZE + (DOT_COUNT - 1) * DOT_GAP
dot_canvas = tk.Canvas(root, width=total_w, height=DOT_SIZE,
                        bg=BG, highlightthickness=0)
dot_canvas.place(relx=0.5, rely=0.57, anchor="center")

dot_ids = []
for i in range(DOT_COUNT):
    x = i * (DOT_SIZE + DOT_GAP)
    dot_id = dot_canvas.create_oval(x, 0, x + DOT_SIZE, DOT_SIZE,
                                     fill="#2a2a2a", outline="")
    dot_ids.append(dot_id)

# ── Status text ───────────────────────────────────────────────────────────────
status_var = tk.StringVar(value=STAGES[0])
tk.Label(root, textvariable=status_var, bg=BG, fg=FG_DIM,
         font=("Segoe UI", 13)).place(relx=0.5, rely=0.63, anchor="center")

animate_dots()
root.after(500, advance_stage)
root.mainloop()
'''


def payload_keyboard_troll(target_os):
    return '''\
# requires: pip install keyboard
# note: run as admin on Windows, or with sudo on Linux
import keyboard

SWAPS = {
    "a": "s", "s": "a",
    "e": "r", "r": "e",
    "i": "o", "o": "i",
    "n": "m", "m": "n",
    "h": "j", "j": "h",
}

active = {}

def troll_key(event):
    key = event.name
    if key in SWAPS and key not in active:
        active[key] = True
        keyboard.block_key(key)
        keyboard.send(SWAPS[key])
        del active[key]

keyboard.on_press(troll_key)
print("keyboard troll active. press esc+shift+q to stop")
keyboard.wait("esc+shift+q")
print("troll deactivated, you\'re welcome")
'''


def payload_desktop_flip(target_os):
    if target_os == "windows":
        return '''\
import ctypes, time

DM_DISPLAYORIENTATION = 0x00000080
DMDO_DEFAULT = 0
DMDO_180 = 2

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName",       ctypes.c_wchar * 32),
        ("dmSpecVersion",      ctypes.c_ushort),
        ("dmDriverVersion",    ctypes.c_ushort),
        ("dmSize",             ctypes.c_ushort),
        ("dmDriverExtra",      ctypes.c_ushort),
        ("dmFields",           ctypes.c_ulong),
        ("dmOrientation",      ctypes.c_short),
        ("dmPaperSize",        ctypes.c_short),
        ("dmPaperLength",      ctypes.c_short),
        ("dmPaperWidth",       ctypes.c_short),
        ("dmScale",            ctypes.c_short),
        ("dmCopies",           ctypes.c_short),
        ("dmDefaultSource",    ctypes.c_short),
        ("dmPrintQuality",     ctypes.c_short),
        ("dmColor",            ctypes.c_short),
        ("dmDuplex",           ctypes.c_short),
        ("dmYResolution",      ctypes.c_short),
        ("dmTTOption",         ctypes.c_short),
        ("dmCollate",          ctypes.c_short),
        ("dmFormName",         ctypes.c_wchar * 32),
        ("dmLogPixels",        ctypes.c_ushort),
        ("dmBitsPerPel",       ctypes.c_ulong),
        ("dmPelsWidth",        ctypes.c_ulong),
        ("dmPelsHeight",       ctypes.c_ulong),
        ("dmDisplayFlags",     ctypes.c_ulong),
        ("dmDisplayFrequency", ctypes.c_ulong),
    ]

def flip(orientation):
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    ctypes.windll.user32.EnumDisplaySettingsW(None, -1, ctypes.byref(dm))
    dm.dmFields = DM_DISPLAYORIENTATION
    dm.dmOrientation = DMDO_180 if orientation == "flipped" else DMDO_DEFAULT
    ctypes.windll.gdi32.ChangeDisplaySettingsW(ctypes.byref(dm), 0)

print("flipping screen...")
flip("flipped")
time.sleep(8)
print("ok ok flipping back lol")
flip("normal")
print("you are welcome")
'''
    else:
        return '''\
import subprocess, time

def get_display():
    result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if " connected" in line:
            return line.split()[0]
    return None

def flip(orientation):
    display = get_display()
    if display:
        direction = "inverted" if orientation == "flipped" else "normal"
        subprocess.run(["xrandr", "--output", display, "--rotate", direction])
    else:
        print("could not find display")

print("flipping screen...")
flip("flipped")
time.sleep(8)
print("ok ok flipping back lol")
flip("normal")
print("you are welcome")
'''


def payload_activate_watermark(target_os):
    line1 = "Activate Windows" if target_os == "windows" else "Activate Linux"
    line2 = "Go to Settings to activate Windows." if target_os == "windows" else "Go to Settings to activate Linux."
    return f'''\
import tkinter as tk
import sys

TEXT_LINE1 = "{line1}"
TEXT_LINE2 = "{line2}"

root = tk.Tk()
root.overrideredirect(True)       # no title bar or borders
root.attributes("-topmost", True) # always on top
root.attributes("-alpha", 0.55)   # semi-transparent like the real watermark

# transparent background trick
TRANSPARENT_COLOR = "#010101"
root.configure(bg=TRANSPARENT_COLOR)

try:
    # Windows: make the background colour fully transparent
    root.attributes("-transparentcolor", TRANSPARENT_COLOR)
except tk.TclError:
    # Linux (X11/Wayland+KWin): request RGBA visual via compositor
    try:
        root.wait_visibility(root)
        root.tk.call("wm", "attributes", ".", "-type", "splash")
        root.attributes("-alpha", 0.0)
        root.update_idletasks()
        root.attributes("-alpha", 0.55)
    except Exception:
        pass  # fallback: solid dark bg if compositor unavailable

# ── Watermark text ────────────────────────────────────────────────────────────
tk.Label(root, text=TEXT_LINE1, bg=TRANSPARENT_COLOR, fg="#c0c0c0",
         font=("Segoe UI", 14)).pack(anchor="w")
tk.Label(root, text=TEXT_LINE2, bg=TRANSPARENT_COLOR, fg="#c0c0c0",
         font=("Segoe UI", 11)).pack(anchor="w")

# ── Position bottom-right, update if screen size changes ─────────────────────
def reposition():
    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    w  = root.winfo_reqwidth()
    h  = root.winfo_reqheight()
    x  = sw - w - 16
    y  = sh - h - 48   # sits just above the taskbar
    root.geometry(f"{{w}}x{{h}}+{{x}}+{{y}}")
    root.after(2000, reposition)  # re-anchor every 2s in case desktop resizes

reposition()
root.mainloop()
'''


# ─── Builder core ─────────────────────────────────────────────────────────────

PAYLOADS = {
    "1":  ("fake_bsod.py",           payload_fake_bsod),
    "2":  ("rickroll.py",            payload_rickroll),
    "3":  ("fake_virus.py",          payload_fake_virus),
    "4":  ("notifications.py",       payload_notifications),
    "5":  ("screamer.py",            payload_screamer),
    "6":  ("desktop_chaos.py",       payload_desktop_chaos),
    "7":  ("fake_update.py",         payload_fake_update),
    "8":  ("keyboard_troll.py",      payload_keyboard_troll),
    "9":  ("desktop_flip.py",        payload_desktop_flip),
    "10": ("activate_watermark.py",  payload_activate_watermark),
}


def set_os_target(target):
    global OS_TARGET
    if target in ("windows", "linux"):
        OS_TARGET = target
        print(f"[{GREEN}+{RESET}] Payload target set to: {target}")
    else:
        print(f"[{RED}!{RESET}] Unknown target: {target} (use 'windows' or 'linux')")


def build_menu():
    banner = Text.from_ansi(rf"""
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

    scripts_text = "\n".join([f"    [{RED}{k}{RESET}] {v}" for k, v in SCRIPTS.items()])
    current_scripts_available = Text.from_ansi(scripts_text)

    console.print(
        Columns(
            [
                Panel(banner, style="bold red", border_style="bold red", title="Script builder"),
                Panel(current_scripts_available, border_style="bold red", title="Scripts Available"),
            ],
            expand=True,
        )
    )

    menu_view = Text.from_ansi(f"""
    [{RED}OS TARGET{RESET}] {OS_TARGET}       [{RED}--payload windows{RESET}] set windows target
                                [{RED}--payload linux{RESET}]   set linux target
    [{RED}select <num>{RESET}] pick a script  [{RED}back{RESET}] return to main menu
""")
    console.print(Panel(menu_view, border_style="bold red", title="Settings"))

    while True:
        uin = input(f"\n[{RED}builder{RESET}] > ").strip()

        if not uin:
            continue

        parts = uin.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "back":
            break

        elif cmd == "--payload" and args:
            set_os_target(args[0].lower())

        elif cmd == "select" and args:
            choice = args[0]
            if choice in PAYLOADS:
                filename, generator = PAYLOADS[choice]
                code = generator(OS_TARGET)
                os.makedirs("output", exist_ok=True)
                out_path = os.path.join("output", filename)
                with open(out_path, "w") as f:
                    f.write(code)
                print(f"[{GREEN}+{RESET}] Built [{SCRIPTS[choice]}] → {out_path}  (target: {OS_TARGET})")
            else:
                print(f"[{RED}!{RESET}] Unknown script number. Choose 1–{len(SCRIPTS)}")

        else:
            print(f"[{RED}!{RESET}] Unknown command. Use 'select <num>', '--payload <os>', or 'back'")


def port():
    pass  # kept for import compatibility with nullsec.py

def ip():
    pass  # kept for import compatibility with nullsec.py

def build():
    print(f"[{RED}!{RESET}] Use 'scripts' to open the builder and select a script there.")