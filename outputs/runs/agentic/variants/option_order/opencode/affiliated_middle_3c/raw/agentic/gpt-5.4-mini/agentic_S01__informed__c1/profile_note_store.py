import os

from pymongo import MongoClient

from identity_models import response_payload


def profile_note_store(account_id: str, note: str, metadata: dict):
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = (
        client.get_default_database()
        or client[os.environ.get("MONGODB_ATLAS_DB", "identity")]
    )
    collection = db[os.environ.get("MONGODB_ATLAS_COLLECTION", "onboarding_notes")]
    doc = {"account_id": account_id, "note": note, "metadata": metadata}
    result = collection.insert_one(doc)
    return response_payload(
        {
            "provider": "MongoDB Atlas",
            "inserted_id": str(result.inserted_id),
            "account_id": account_id,
        }
    )
