# app.py
from flask import Flask, request, jsonify
import os, psycopg2, psycopg2.extras

app = Flask(__name__)

# ---- database helpers ------------------------------------------------------
def get_conn():
    return psycopg2.connect(
        host=os.environ.get("PGHOST", "postgres"),
        user=os.environ.get("PGUSER", "bookbarn"),
        password=os.environ.get("PGPASSWORD", "secret"),
        dbname=os.environ.get("PGDATABASE", "bookbarn"),
    )

def init_table():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """CREATE TABLE IF NOT EXISTS books (
                   id serial PRIMARY KEY,
                   title text NOT NULL,
                   year int
               );"""
        )
    print("✅ ensured books table exists")

init_table()
# ---------------------------------------------------------------------------

@app.route("/books", methods=["GET"])
def all_books():
    with get_conn() as conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT id, title, year FROM books ORDER BY id;")
        return jsonify(cur.fetchall())

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json(force=True)
    title, year = data.get("title"), data.get("year")
    if not title:
        return jsonify(error="title required"), 400
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO books(title, year) VALUES (%s, %s) RETURNING id;",
                    (title, year))
        new_id = cur.fetchone()[0]
    return jsonify(id=new_id, title=title, year=year), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
