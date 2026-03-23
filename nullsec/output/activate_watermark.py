import tkinter as tk
import sys

TEXT_LINE1 = "Activate Linux"
TEXT_LINE2 = "Go to Settings to activate Linux."

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
        root.attributes("-alpha", 0.15)
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
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.after(2000, reposition)  # re-anchor every 2s in case desktop resizes

reposition()
root.mainloop()
