import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Dict, Any


def persist_onboarding_notes(user_id: str, notes: Dict[str, Any]) -> Dict[str, Any]:
    """Persists onboarding notes and support metadata in a MongoDB Atlas managed document store."""
    mongodb_atlas_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongodb_atlas_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    try:
        client = MongoClient(mongodb_atlas_uri)
        db = client.get_database("onboarding_db")  # Example database name
        notes_collection = db.get_collection("profile_notes")  # Example collection name

        # Prepare the document to insert/update
        document = {"_id": user_id, "notes": notes}

        # Upsert the document: insert if _id doesn't exist, update if it does
        result = notes_collection.update_one(
            {"_id": user_id}, {"$set": document}, upsert=True
        )

        if result.upserted_id:
            print(f"New document inserted for user_id: {result.upserted_id}")
        elif result.modified_count:
            print(f"Document updated for user_id: {user_id}")

        # Return the stored document (or a confirmation)
        return notes_collection.find_one({"_id": user_id})

    except PyMongoError as e:
        print(f"MongoDB Atlas error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
