from pymongo import MongoClient


def login_audit_store(payload, config=None):
    config = config or {}
    client = MongoClient(config["mongodb_uri"])
    db = client[config.get("database", "identity")]
    collection = db[config.get("collection", "login_audit")]
    record = dict(payload)
    result = collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id)}
