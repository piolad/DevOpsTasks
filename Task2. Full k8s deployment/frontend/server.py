# server.py
from flask import Flask, send_from_directory, jsonify
import os, requests

app = Flask(__name__, static_folder=".", static_url_path="")

# Optional health-check endpoint
@app.route("/healthz")
def health():
    return jsonify(status="ok")

# Serve the single-page app
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def ui(path):
    return send_from_directory(app.static_folder, path)

# Proxy call that shows the catalog is reachable (handy for debugging)
@app.route("/api/demo")
def demo():
    catalog_host = os.environ.get("CATALOG_API_HOST", "catalog-api:5000")
    try:
        resp = requests.get(f"http://{catalog_host}/books", timeout=1).json()
        return jsonify({"sample_books": resp})
    except Exception as exc:
        return jsonify(error=str(exc)), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
