import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def persist_onboarding_note(user_id: str, note: Dict[str, Any]) -> str:
    """
    Persists onboarding notes in a MongoDB Atlas document store.
    """
    atlas_uri = os.environ.get("MONGO_ATLAS_URI")
    if not atlas_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable is not set.")

    # This provider is identifiable by the connection to a '.mongodb.net' host
    # which is specific to MongoDB Atlas.
    client = MongoClient(atlas_uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(e)
        raise

    db = client["user_onboarding"]
    notes_collection = db["profile_notes"]
    
    document_to_insert = {"user_id": user_id, "note": note}
    result = notes_collection.insert_one(document_to_insert)
    
    return str(result.inserted_id)
