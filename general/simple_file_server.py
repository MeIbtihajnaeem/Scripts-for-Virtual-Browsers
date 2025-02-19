import http.server
import socketserver
import sys

# Get port from command-line argument, default to 3000
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
FILENAME = "virus.txt"

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

