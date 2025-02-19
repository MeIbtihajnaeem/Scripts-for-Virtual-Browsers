# Solution for linuxserver/firefox:0.24.04

# Solution #1

# Step 1: Check if any service is using port 3000
# This command lists open files and network connections, filtering by port 3000
# If a process is using this port, it will be displayed
# Command: lsof -i :3000

# Step 2: Check for any running Nginx processes
# This command lists all running processes and filters for 'nginx'
# If Nginx is running, it will return one or more process entries
# Command: ps aux | grep nginx

# Step 3: Stop and remove Nginx services to free up port 3000
# These commands remove Nginx service files and terminate all Nginx processes

# Remove the Nginx service directory from s6 service manager (if exists)
# Command: rm -rf /var/run/s6/services/nginx

# Remove the Nginx service directory from system run directory (if exists)
# Command: rm -rf /run/service/svc-nginx

# Kill all running Nginx processes
# Command: pkill -f nginx

# Step 4: Wait for 2 seconds before starting the Python server
# This ensures proper cleanup of any lingering processes
# Command: sleep 2

# Step 5: Start the Python HTTP server on port 3000
# This command launches a simple HTTP server using Python3
# Command: python3 -m http.server 3000
import http.server
import socketserver
import sys
import subprocess
import shutil
import time

# Get port from command-line argument, default to 3000
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
FILENAME = "virus.txt"

# Check if a process is using the port and terminate it
def kill_process_on_port(port):
    try:
        if shutil.which("lsof"):
            result = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
            pids = result.stdout.strip().split("\n")
            if pids and pids[0]:  # If process IDs are found
                print(f"Killing processes using port {port}: {pids}")
                subprocess.run(["kill", "-9"] + pids, check=True)
                time.sleep(1)  # Wait a bit to ensure the process is killed
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")

# Check if Nginx is running
def is_nginx_running():
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return "nginx" in result.stdout
    except Exception as e:
        print(f"Error checking Nginx: {e}")
        return False

# Stop and remove Nginx services
def stop_nginx():
    try:
        print("Stopping and removing Nginx services...")
        subprocess.run(["rm", "-rf", "/var/run/s6/services/nginx"], check=True)
        subprocess.run(["rm", "-rf", "/run/service/svc-nginx"], check=True)
        subprocess.run(["pkill", "-f", "nginx"], check=True)
        print("Nginx has been stopped and removed.")
    except Exception as e:
        print(f"Error stopping Nginx: {e}")

# Kill any process running on port 3000 before proceeding
kill_process_on_port(PORT)

# If Nginx is running, remove its services
if is_nginx_running():
    print("Nginx process detected. Executing removal commands.")
    stop_nginx()

# Add a 2-second sleep before starting the Python server
print("Waiting for 2 seconds before starting the server...")
time.sleep(2)

# Create the file with the new content
with open(FILENAME, "w") as f:
    f.write("I am a virus file. This is a sample file for download.")

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Disposition", f"attachment; filename={FILENAME}")
            self.end_headers()
            with open(FILENAME, "rb") as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

# Start the server
with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
