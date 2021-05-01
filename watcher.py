import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import hashlib
import hmac
import traceback

config = {}
try:
    with open("./config.json") as file:
        config = json.load(file)
except:
    print("Cannot find config.json!")
    exit(1)

if (__name__ != "__main__"):
    exit(1)

def pull(repo):
    """Fuction called when the hook is called."""
    print("Hook called.")
    try:
        os.system(f"cd {repo['directory']} && git reset --hard && git pull && {repo['command']}")
        print("Pulled and executed command!")
    except:
        traceback.print_exc()
        print("Cannot execute command, check directory path or command. Check that you can git pull the given repo without credentials.")

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler class."""

    def do_POST(self):
        """Handle POST request."""
        if (self.path == "/push"):
            try:
                length = int(self.headers["content-length"])
                body = self.rfile.read(length)
                message = json.loads(body)
                branch = message["ref"].replace("refs/heads/", "")
                for repo in config["repos"]:
                    if (repo["repo"] == message["repository"]["full_name"]):
                        hash = hmac.new(bytes(repo["secret"], "utf-8"), body, hashlib.sha1)
                        hash = hash.hexdigest()
                        hash_received = self.headers["X-Hub-Signature"].split("sha1=")[1]
                        if (branch == repo["branch"] and hash_received == hash):
                            pull(repo)
                        else:
                            print("Wrong secret or branch.")
            except:
                traceback.print_exc()
                print("Cannot process request.")

server_address = ("0.0.0.0", 9999)
httpd = HTTPServer(server_address, RequestHandler)
print(f"Listening to push hooks on port 9999.")
httpd.serve_forever()