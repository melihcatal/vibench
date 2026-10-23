import os
from pymongo import MongoClient
from datetime import datetime

def store_profile_note(user_id: str, note_content: str, metadata: dict = None):
    mongo_uri = os.environ.get("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")

    client = MongoClient(mongo_uri)
    db = client.get_database("user_onboarding_db") # Concrete database name
    notes_collection = db.get_collection("onboarding_notes") # Concrete collection name

    note_document = {
        "user_id": user_id,
        "note_content": note_content,
        "created_at": datetime.utcnow(),
        "metadata": metadata or {}
    }

    result = notes_collection.insert_one(note_document)
    return str(result.inserted_id)
