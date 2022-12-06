from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# TODO: import kube lib and delete the pv 

class Controller(BaseHTTPRequestHandler):

    def do_POST(self):
        observed = json.loads(self.rfile.read(
            int(self.headers.get("content-length"))))
        observed_pv_map = observed["children"].get(
            "Pv/v1", {})

        finalized = len(observed_pv_map) == 0
        desired = {
            "finalized": finalized
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(desired).encode())


HTTPServer(("", 9090), Controller).serve_forever()