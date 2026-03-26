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
