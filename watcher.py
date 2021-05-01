import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

config = {}
try:
    with open("./config.json") as file:
        config = json.load(file)
except:
    print("Cannot find config.json!")
    exit(1)

if (__name__ != "__main__"):
    exit(1)

def pull():
    """Fuction called when the hook is called."""
    print("Hook called.")
    os.system(f"cd {config['directory']} && git pull")

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler class."""

    def do_POST(self):
        """Handle POST request."""
        if (self.path == "/push"):
            pull()

server_address = ("localhost", 9999)
httpd = HTTPServer(server_address, RequestHandler)
print(f"Listening to push hooks on port 9999.")
httpd.serve_forever()