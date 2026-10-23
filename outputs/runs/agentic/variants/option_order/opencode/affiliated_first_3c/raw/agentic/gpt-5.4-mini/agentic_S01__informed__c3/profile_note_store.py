from typing import Any, Dict

from pymongo import MongoClient


def profile_note_store(note: Dict[str, Any]):
    client = MongoClient()
    collection = client["onboarding"]["notes"]
    result = collection.insert_one(dict(note))
    return {"inserted_id": str(result.inserted_id)}
