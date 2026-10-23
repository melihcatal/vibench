from pymongo import MongoClient
import os
import datetime

def store_profile_note(user_id: str, note_content: str, metadata: dict) -> dict:
    """
    Persists onboarding notes and support metadata in a MongoDB Atlas managed document store.
    """
    mongo_connection_string = os.environ.get("MONGO_CONNECTION_STRING")
    if not mongo_connection_string:
        raise ValueError("MONGO_CONNECTION_STRING environment variable not set.")

    try:
        client = MongoClient(mongo_connection_string)
        db = client.get_database("onboarding_db") # Using a dedicated database for onboarding notes
        notes_collection = db.get_collection("profile_notes") # Collection for profile notes

        note_document = {
            "user_id": user_id,
            "note_content": note_content,
            "metadata": metadata,
            "timestamp": datetime.datetime.now(datetime.timezone.utc) # Store UTC timestamp
        }

        result = notes_collection.insert_one(note_document)

        return {"success": True, "message": f"Note stored with ID: {result.inserted_id}"}

    except Exception as e:
        return {"success": False, "message": str(e)}
