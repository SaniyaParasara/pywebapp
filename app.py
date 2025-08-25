import os
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

PORT = int(os.getenv("PORT", "8000"))
MONGO_URL = os.getenv("MONGO_URL")  # e.g., mongodb://localhost:27017/webapp

# Optional MongoDB support (falls back to in-memory if not available)
items_mem = []
db_items = None

try:
    if MONGO_URL:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")  # quick connectivity check

        # choose DB name: if URL has a trailing "/<db>", use it; else default to "webapp"
        tail = MONGO_URL.split("//", 1)[-1]
        dbname = tail.split("/", 1)[-1] if "/" in tail else "webapp"
        if not dbname:
            dbname = "webapp"
        db = client[dbname]
        db_items = db["items"]
        app.logger.info("[mongo] connected")
    else:
        app.logger.info("[mongo] MONGO_URL not set; using in-memory store")
except Exception as e:
    app.logger.warning(f"[mongo] connect failed (app will still run): {e}")
    db_items = None

@app.get("/")
def home():
    return "Hello from Python WebApp 🚀 CI/CD (Gunicorn + Compose + Jenkins)"

@app.get("/healthz")
def healthz():
    # add a simple check for DB connectivity if configured
    if db_items is not None:
        try:
            # ping once in a while
            db_items.database.client.admin.command("ping")
        except Exception as e:
            return jsonify(status="degraded", db="down", error=str(e)), 200
    return jsonify(status="ok"), 200

@app.get("/api/items")
def get_items():
    if db_items is not None:
        docs = list(db_items.find().sort("created_at", -1))
        for d in docs:
            d.pop("_id", None)
        return jsonify(docs)
    return jsonify(items_mem)

@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify(error="name is required"), 400

    if db_items is not None:
        doc = {"name": name, "created_at": datetime.utcnow()}
        db_items.insert_one(doc)
        doc.pop("_id", None)
        return jsonify(doc), 201

    item = {"name": name, "created_at": datetime.utcnow().isoformat() + "Z"}
    items_mem.append(item)
    return jsonify(item), 201

if __name__ == "__main__":
    # Dev server (use gunicorn in Docker)
    app.run(host="0.0.0.0", port=PORT)
