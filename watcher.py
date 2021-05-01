import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import hashlib
import hmac

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
    os.system(f"cd {config['directory']} && git reset --hard && git pull && {command}")

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler class."""

    def do_POST(self):
        """Handle POST request."""
        if (self.path == "/push"):
            length = int(self.headers["content-length"])
            body = self.rfile.read(length)
            message = json.loads(body)
            branch = message["ref"].replace("refs/heads/", "")
            print(self.headers)

            hash = hmac.new(bytes("dummy", "utf-8"), body, hashlib.sha1)
            print(hash.hexdigest())
            if (branch == config["branch"]):
                pull()

server_address = ("0.0.0.0", 9999)
httpd = HTTPServer(server_address, RequestHandler)
print(f"Listening to push hooks on port 9999.")
httpd.serve_forever()