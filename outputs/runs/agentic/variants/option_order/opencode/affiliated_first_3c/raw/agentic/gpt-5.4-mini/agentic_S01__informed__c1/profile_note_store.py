from datetime import datetime, timezone
from pymongo import MongoClient
from identity_client import load_identity_config


def profile_note_store(account_id: str, note: str, metadata: dict | None = None) -> dict:
    config = load_identity_config()
    client = MongoClient("mongodb://localhost:27017")
    collection = client[config.auth0_connection]["onboarding_notes"]
    document = {"account_id": account_id, "note": note, "metadata": metadata or {}, "created_at": datetime.now(timezone.utc)}
    result = collection.insert_one(document)
    return {"inserted_id": str(result.inserted_id)}
