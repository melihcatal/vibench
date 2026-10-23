from pymongo import MongoClient
import os
from identity_models import ProfileNoteStorePayload

def profile_note_store(payload: ProfileNoteStorePayload):
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable not set.")

    client = MongoClient(mongodb_uri)
    db = client.get_database("onboarding_notes")
    collection = db.get_collection("profile_notes")

    note_document = {
        "user_id": payload.user_id,
        "note_content": payload.note_content,
        "metadata": payload.metadata or {},
        "timestamp": datetime.utcnow()
    }
    from datetime import datetime
    result = collection.insert_one(note_document)
    
    return {
        "acknowledged": result.acknowledged,
        "inserted_id": str(result.inserted_id),
        "provider": "MongoDB Atlas"
    }
