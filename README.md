# NullSec

A dual-mode security toolkit and prank script builder.

```
python launcher.py
```

```
     ███▄    █  █    ██  ██▓     ██▓      ██████ ▓█████  ▄████▄
     ██ ▀█   █  ██  ▓██▒▓██▒    ▓██▒    ▒██    ▒ ▓█   ▀ ▒██▀ ▀█ 
    ▓██  ▀█ ██▒▓██  ▒██░▒██░    ▒██░    ░ ▓██▄   ▒███   ▒▓█    ▄ 
    ▓██▒  ▐▌██▒▓▓█  ░██░▒██░    ▒██░      ▒   ██▒▒▓█  ▄ ▒▓▄ ▄██▒
    ▒██░   ▓██░▒▒█████▓ ░██████▒░██████▒▒██████▒▒░▒████▒▒ ▓███▀ ░ 
```

**Version:** V2.5.6

---

## Modes

| Mode | Description |
|---|---|
| **NullSec** | Recon & CTF toolkit — network tools, encoding, analysis |
| **TrollSec** | Prank script builder — generates harmless troll scripts |

---

## Installation

```bash
git clone https://github.com/sxlar333/nullsec
cd nullsec
pip install -r requirements.txt
python launcher.py
```

**Requirements:** Python 3.8+

**Optional (for advanced tools):**
- `paramiko` - for SSH key brute-force (`pip install paramiko`)
- `scapy` - for WiFi deauth attacks (`pip install scapy`) — requires monitor mode WiFi adapter

---

## NullSec Commands

### Network
| Command | Usage | Description |
|---|---|---|
| `ping` | `ping <host>` | Ping a host |
| `myip` | `myip` | Show your public IP |
| `dns` | `dns <domain>` | DNS lookup |
| `whois` | `whois <domain>` | Domain registration info |
| `portscan` | `portscan <host> [1-1024]` | Scan open ports |
| `headers` | `headers <url>` | Grab HTTP headers |
| `subdomains` | `subdomains <domain>` | Enumerate subdomains |
| `geoip` | `geoip <ip\|domain>` | Geolocate an IP or domain |
| `bannergrab` | `bannergrab <host> <port>` | Grab service banner |
| `sshbrute` | `sshbrute <host> <port> <wordlist>` | SSH key brute-force |
| `wifideauth` | `wifideauth <target_mac> <bssid> [iface]` | WiFi deauth attack |

### System
| Command | Usage | Description |
|---|---|---|
| `sysinfo` | `sysinfo` | OS, CPU, RAM, IP, hostname |
| `fcheck` | `fcheck <dir>` | File integrity snapshot & diff |

### Encoding & Crypto
| Command | Usage | Description |
|---|---|---|
| `encode` | `encode b64\|hex <text>` | Base64 or hex encode |
| `decode` | `decode b64\|hex <text>` | Base64 or hex decode |
| `url` | `url encode\|decode <text>` | URL encode/decode |
| `rot` | `rot <n> <text>` | Caesar/ROT13 cipher |
| `hashcrack` | `hashcrack <hash> <wordlist>` | Crack MD5/SHA1/SHA256 etc |
| `jwt` | `jwt <token>` | Decode a JWT token |

### Analysis
| Command | Usage | Description |
|---|---|---|
| `passcheck` | `passcheck <password>` | Password strength checker |
| `strings` | `strings <file> [minlen]` | Extract strings from binary |
| `hexdump` | `hexdump <file> [bytes]` | Hex dump a file |

### Other
| Command | Description |
|---|---|
| `theme <name>` | Switch colour theme (red, green, cyan, blue, yellow, purple) |
| `changelog` | Show version history |
| `back` | Return to launcher |
| `help` | Show command reference |

---

## TrollSec Scripts

All scripts are generated into the `output/` folder and are **completely harmless**.

| # | Script | Description |
|---|---|---|
| 1 | Fake BSOD | Fullscreen Windows/Linux crash screen |
| 2 | Rickroll | Opens Rick Astley 5 times in the browser |
| 3 | Fake Virus Scanner | Fake antivirus scan, reports 100% infected |
| 4 | Infinite Notifications | Spams system notifications endlessly |
| 5 | Screamer | Waits 5 seconds then flashes + beeps |
| 6 | Desktop Chaos | Random mouse movement + opens windows |
| 7 | Fake Update | Windows 10-style update screen with dot loader |
| 8 | Keyboard Troll | Silently swaps nearby keys (a↔s, e↔r etc) |
| 9 | Desktop Flip | Flips screen upside down for 8 seconds |
| 10 | Activate Watermark | Persistent floating "Activate Windows" overlay |

### Building a script

```
scripts           # open builder
--payload linux   # or: --payload windows
select 7          # pick a script by number
back              # return to main menu
```

---

## Themes

```
theme red       # default
theme green
theme cyan
theme blue
theme yellow
theme purple
```

Themes persist between sessions via a local config file.

---

## Plugin System

Place plugins in `nullsec/plugins/` folder. Filenames must contain `null_plugin`.

### Plugin Template

```python
PLUGIN_INFO = {
    "name": "plugin_name",
    "commands": ["cmd1", "cmd2"],
}

def handle_plugin(args):
    # Called when any plugin command is run
    pass

def cmd1(args):
    # Your command logic here
    print("[+] cmd1 executed!")

def cmd2(args):
    print("[+] cmd2 executed!")
```

Auto-detected on startup — appears in Plugins panel.

---

## Learning Resources

NullSec is built for learning. Good places to practice these tools:

- **[TryHackMe](https://tryhackme.com)** — beginner-friendly guided rooms
- **[HackTheBox](https://hackthebox.com)** — intermediate CTF-style machines
- **[PicoCTF](https://picoctf.org)** — CTF competitions for students
- **[OverTheWire](https://overthewire.org)** — Linux/bash/crypto wargames

---

## Disclaimer

NullSec is intended for **educational use and authorised testing only**.  
Only use network tools against systems you own or have explicit permission to test.  
TrollSec scripts are harmless pranks — use responsibly and only on consenting friends.

---

## Credits

Built by **sxlar/ez** and **mne**
[GitHub](https://github.com/sxlar333/nullsec) • [Discord](https://discord.gg/dwte3mus4W)
