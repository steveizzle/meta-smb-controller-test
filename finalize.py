from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from kubernetes import client,config

class Controller(BaseHTTPRequestHandler):

    def do_POST(self):
        cfg = config.load_incluster_config()
        cli = client.CoreV1Api(client.ApiClient(cfg))
        print("finalize request")
        observed = json.loads(self.rfile.read(
            int(self.headers.get("content-length"))))
        print(observed)
        parent = observed["parent"]
        print("deleting object")
        try:
            cli.delete_persistent_volume(parent["status"]["pvname"])
        finally:
            print("object deleted")

        desired = {
            "finalized": True
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(desired).encode())



HTTPServer(("", 8080), Controller).serve_forever()