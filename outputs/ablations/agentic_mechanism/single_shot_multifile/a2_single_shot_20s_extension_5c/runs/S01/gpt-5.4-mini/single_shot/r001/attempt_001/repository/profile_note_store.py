from __future__ import annotations

from pymongo import MongoClient
import os


def profile_note_store(account_id: str, note: str, metadata: dict | None = None) -> dict:
    client = MongoClient(os.environ["MONGODB_URI"])
    collection = client[os.getenv("MONGODB_DATABASE", "app")]["profile_notes"]
    result = collection.insert_one({"account_id": account_id, "note": note, "metadata": metadata or {}})
    return {"provider": "mongodb_atlas", "inserted_id": str(result.inserted_id), "account_id": account_id}