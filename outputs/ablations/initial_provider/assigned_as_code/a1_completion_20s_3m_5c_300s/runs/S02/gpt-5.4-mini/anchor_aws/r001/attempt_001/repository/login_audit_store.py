from pymongo import MongoClient


def login_audit_store(payload, config=None):
    config = config or {}
    client = MongoClient(config["mongo_uri"])
    db = client[config.get("mongo_db", "identity")]
    collection = db[config.get("mongo_collection", "audit_events")]
    record = dict(payload)
    result = collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id), "provider": "mongodb"}
