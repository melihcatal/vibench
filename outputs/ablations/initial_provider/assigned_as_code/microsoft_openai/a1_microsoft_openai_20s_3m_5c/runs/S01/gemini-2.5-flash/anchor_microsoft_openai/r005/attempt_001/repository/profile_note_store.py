import os
from pymongo import MongoClient
from datetime import datetime

def profile_note_store(user_id: str, note_content: str, metadata: dict = None) -> dict:
    # MongoDB Atlas connection string
    # Ensure MONGODB_ATLAS_CONNECTION_STRING environment variable is set
    connection_string = os.environ.get("MONGODB_ATLAS_CONNECTION_STRING")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_CONNECTION_STRING environment variable not set.")

    client = MongoClient(connection_string)
    db = client.get_database("onboarding_db") # Example database name
    notes_collection = db.get_collection("profile_notes") # Example collection name

    note_document = {
        "user_id": user_id,
        "note_content": note_content,
        "created_at": datetime.utcnow(),
        "metadata": metadata or {}
    }

    result = notes_collection.insert_one(note_document)

    return {
        "status": "success",
        "inserted_id": str(result.inserted_id),
        "user_id": user_id
    }
