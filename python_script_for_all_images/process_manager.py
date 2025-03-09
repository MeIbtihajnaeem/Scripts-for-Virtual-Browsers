import os
import shutil
import subprocess
import asyncio
import platform

OLD_NGINX_PATHS = []
NEW_NGINX_PATHS = []

class ProcessManager:
    def __init__(self, port, nginx_backup_dir="/var/backups/nginx/"):
        self.port = port
        self.nginx_backup_dir = nginx_backup_dir
        os.makedirs(self.nginx_backup_dir, exist_ok=True)  # Ensure backup directory exists

    async def kill_process_on_port(self):
        """Asynchronously kills any process using the specified port."""
        try:
            if shutil.which("lsof"):
                process = await asyncio.create_subprocess_exec(
                    "lsof", "-ti", f":{self.port}",
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                stdout, _ = await process.communicate()
                pids = stdout.decode().strip().split("\n")

                if pids and pids[0]:  # If process IDs are found
                    print(f"Killing processes using port {self.port}: {pids}")
                    await asyncio.create_subprocess_exec("kill", "-9", *pids)
                    await asyncio.sleep(1)  # Allow some time for process termination

        except Exception as e:
            print(f"Error killing process on port {self.port}: {e}")

    async def is_nginx_running(self):
        """Asynchronously checks if Nginx is currently running."""
        try:
            process = await asyncio.create_subprocess_exec(
                "ps", "aux",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            return "nginx" in stdout.decode()
        except Exception as e:
            print(f"Error checking Nginx: {e}")
            return False

    def detect_os(self):
        """Detects the operating system and returns the distribution ID (Ubuntu, Debian, Alpine, etc.)."""
        try:
            if os.path.exists("/etc/os-release"):
                with open("/etc/os-release") as f:
                    lines = f.readlines()
                    os_info = {line.split("=")[0]: line.split("=")[1].strip().strip('"') for line in lines if "=" in line}
                    return os_info.get("ID", "unknown").lower()  # Return OS ID (e.g., 'ubuntu', 'debian', 'alpine')
            return "unknown"
        except Exception as e:
            print(f"Error detecting OS: {e}")
            return "unknown"

    async def stop_nginx(self):
        """Asynchronously stops Nginx and moves service files to a backup directory instead of deleting them."""
        global OLD_NGINX_PATHS, NEW_NGINX_PATHS
        try:
            os_type = self.detect_os()
            print(f"Detected OS: {os_type}")

            # Adjust Nginx paths based on OS type
            if os_type == "alpine":
                nginx_paths = ["/opt/base/sbin/nginx"]
            else:
                nginx_paths = ["/var/run/s6/services/nginx", "/run/service/svc-nginx"]

            print("Stopping Nginx services...")

            for path in nginx_paths:
                if os.path.exists(path):
                    backup_path = os.path.join(self.nginx_backup_dir, os.path.basename(path))

                    # Store paths in global variables
                    OLD_NGINX_PATHS.append(path)
                    NEW_NGINX_PATHS.append(backup_path)

                    print(f"Moving {path} to {backup_path}")
                    shutil.move(path, backup_path)

            await asyncio.create_subprocess_exec("pkill", "-f", "nginx")
            print("✅ Nginx has been stopped and moved to backup.")

        except Exception as e:
            print(f"❌ Error stopping Nginx: {e}")
