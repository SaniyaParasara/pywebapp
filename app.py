import os
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
        db = client.get_database() if "/" in MONGO_URL.split("//", 1)[-1] else client["webapp"]
        db_items = db["items"]
        app.logger.info("[mongo] connected")
except Exception as e:
    app.logger.warning(f"[mongo] connect failed (app will still run): {e}")

@app.get("/")
def home():
    return "Hello from Python WebApp 🚀"

@app.get("/healthz")
def healthz():
    return jsonify(status="ok"), 200

@app.get("/api/items")
def get_items():
    if db_items is not None:
        docs = list(db_items.find().sort("created_at", -1))
        # strip _id for clean JSON
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
        doc = {"name": name}
        db_items.insert_one(doc)
        doc.pop("_id", None)
        return jsonify(doc), 201

    item = {"name": name}
    items_mem.append(item)
    return jsonify(item), 201

if __name__ == "__main__":
    # Dev server (use gunicorn in Docker)
    app.run(host="0.0.0.0", port=PORT)



