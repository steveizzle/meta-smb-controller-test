from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Controller(BaseHTTPRequestHandler):
  def sync(self, parent, children):
    # Compute status based on observed state.
    print("children:")
    print(children)
    desired_status = {
      "pvcs": len(children["PersistentVolumeClaim.v1"])
    }
    print("desired status:")
    print(desired_status)

    # Generate the desired child object(s).
    # who = parent.get("spec", {}).get("who", "World")
    desired_volumes = [
      {
        "apiVersion": "v1",
        "kind": "PersistentVolumeClaim",
        "metadata": {
          "name": parent["metadata"]["name"]
        },
        "spec": {
          "accessModes": ["ReadWriteMany"],
          "resources": {
            "requests": {
              "storage": "100Gi"
            }
          },
          "storageClassName": "",
          "volumeMode": "Filesystem",
          "volumeName": "smb-%s-%s" % (parent["metadata"]["namespace"], parent["metadata"]["name"]),
        }
      },
      {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
          "name": "smb-%s-%s" % (parent["metadata"]["namespace"], parent["metadata"]["name"]),
        },
        "spec": {
          "accessModes": ["ReadWriteMany"],
          "capacity": {
              "storage": "100Gi"
          },
          "mountOptions": parent["spec"]["mountOptions"],
          "csi": {
            "driver": "smb.csi.k8s.io",
            "nodeStageSecretRef": {
              "name": parent["spec"]["secretName"],
              "namespace": parent["metadata"]["namespace"]
            },
            "volumeAttributes": {
              "source": parent["spec"]["path"],
            },
            "volumeHandle": "smb-%s-%s" % (parent["metadata"]["namespace"], parent["metadata"]["name"]),
          },
          "persistentVolumeReclaimPolicy": "Delete",
          "volumeMode": "Filesystem",
        }
      }
    ]

    return {"status": desired_status, "children": desired_volumes}

  def do_POST(self):
    # Serve the sync() function as a JSON webhook.
    observed = json.loads(self.rfile.read(int(self.headers.get("content-length"))))
    print("observed: ")
    print(observed)
    desired = self.sync(observed["parent"], observed["children"])
    print("desired:")
    print(desired)
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(desired).encode())

HTTPServer(("", 80), Controller).serve_forever()
