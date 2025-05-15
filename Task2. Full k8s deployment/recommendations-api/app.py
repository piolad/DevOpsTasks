# app.py
from flask import Flask, jsonify
import os, random, requests

app = Flask(__name__)

@app.route("/recommendations")
def recs():
    # Ask the catalog for its full list, then pick three at random
    catalog_host = os.environ.get("CATALOG_API_HOST", "catalog-api:5000")
    try:
        books = requests.get(f"http://{catalog_host}/books", timeout=1).json()
        picks = random.sample(books, k=min(3, len(books))) if books else []
        return jsonify(recommendations=picks)
    except Exception as exc:
        return jsonify(error=str(exc)), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
