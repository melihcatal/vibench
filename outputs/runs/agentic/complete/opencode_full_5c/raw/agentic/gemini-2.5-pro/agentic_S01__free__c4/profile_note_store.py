import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def store_onboarding_note(user_id: str, note_data: dict):
    atlas_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not atlas_uri:
        raise ValueError("MONGODB_ATLAS_URI not set.")

    client = MongoClient(atlas_uri, server_api=ServerApi("1"))

    try:
        client.admin.command("ping")
    except Exception as e:
        raise Exception(f"Failed to connect to MongoDB Atlas: {e}")

    db = client.onboarding_db
    notes_collection = db.profile_notes

    document = {"user_id": user_id, **note_data}
    result = notes_collection.insert_one(document)

    return str(result.inserted_id)
