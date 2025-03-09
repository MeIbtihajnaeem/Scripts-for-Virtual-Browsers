import os
import sys
import psutil
from flask import Flask, send_file, render_template
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
