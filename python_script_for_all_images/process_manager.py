import os
import shutil
import subprocess
import time

# Global variables to store old and new Nginx paths
OLD_NGINX_PATHS = []
NEW_NGINX_PATHS = []

class ProcessManager:
    def __init__(self, port, nginx_backup_dir="/var/backups/nginx/"):
        self.port = port
        self.nginx_backup_dir = nginx_backup_dir
        os.makedirs(self.nginx_backup_dir, exist_ok=True)  # Ensure backup directory exists

    def kill_process_on_port(self):
        """Kills any process using the specified port."""
        try:
            if shutil.which("lsof"):
                result = subprocess.run(["lsof", "-ti", f":{self.port}"], capture_output=True, text=True)
                pids = result.stdout.strip().split("\n")
                if pids and pids[0]:  # If process IDs are found
                    print(f"Killing processes using port {self.port}: {pids}")
                    subprocess.run(["kill", "-9"] + pids, check=True)
                    time.sleep(1)  # Wait a bit to ensure the process is killed
        except Exception as e:
            print(f"Error killing process on port {self.port}: {e}")

    def is_nginx_running(self):
        """Checks if Nginx is currently running."""
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            return "nginx" in result.stdout
        except Exception as e:
            print(f"Error checking Nginx: {e}")
            return False

    def stop_nginx(self):
        """Stops Nginx and moves service files to a backup directory instead of deleting them."""
        global OLD_NGINX_PATHS, NEW_NGINX_PATHS
        try:
            print("Stopping Nginx services...")

            nginx_paths = ["/var/run/s6/services/nginx", "/run/service/svc-nginx"]
            for path in nginx_paths:
                if os.path.exists(path):
                    backup_path = os.path.join(self.nginx_backup_dir, os.path.basename(path))
                    
                    # Store paths in global variables
                    OLD_NGINX_PATHS.append(path)
                    NEW_NGINX_PATHS.append(backup_path)

                    print(f"Moving {path} to {backup_path}")
                    shutil.move(path, backup_path)

            subprocess.run(["pkill", "-f", "nginx"], check=True)
            print("Nginx has been stopped and moved to backup.")

        except Exception as e:
            print(f"Error stopping Nginx: {e}")


