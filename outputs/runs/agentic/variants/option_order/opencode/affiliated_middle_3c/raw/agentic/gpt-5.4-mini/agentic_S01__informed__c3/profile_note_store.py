from pymongo import MongoClient


def profile_note_store(note: dict):
    client = MongoClient(__import__("os").environ["MONGODB_ATLAS_URI"])
    db = client.get_default_database()
    result = db.onboarding_notes.insert_one(note)
    return {"inserted_id": str(result.inserted_id)}
