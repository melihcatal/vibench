from pymongo import MongoClient

from identity_models import response_payload


def profile_note_store(note: dict):
    client = MongoClient(__import__("os").environ.get("MONGODB_ATLAS_URI", ""))
    db = client.get_default_database()
    collection = db.get_collection("onboarding_notes")
    result = collection.insert_one(note)
    return response_payload(
        "MongoDB Atlas", "profile_note_store", {"inserted_id": str(result.inserted_id)}
    )
