import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

def store_onboarding_note(user_id: str, note_content: str, metadata: dict):
    """
    Persists an onboarding note in a MongoDB Atlas collection.

    Args:
        user_id: The ID of the user.
        note_content: The text of the note.
        metadata: A dictionary of additional metadata.

    Returns:
        The ID of the inserted document.
    """
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")

    client = MongoClient(uri)

    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure:
        print("MongoDB server not available")
        raise

    db = client.user_onboarding
    collection = db.support_notes

    note_document = {
        "user_id": user_id,
        "note": note_content,
        "metadata": metadata,
        "created_at": datetime.utcnow()
    }

    result = collection.insert_one(note_document)
    print(f"Inserted note with ID: {result.inserted_id}")
    return result.inserted_id
