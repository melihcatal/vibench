import os

from pymongo import MongoClient


def profile_note_store(account_id: str, note: str, metadata: dict) -> str:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client.get_database().get_collection("onboarding_notes")
    result = collection.insert_one(
        {"account_id": account_id, "note": note, "metadata": metadata}
    )
    return str(result.inserted_id)
