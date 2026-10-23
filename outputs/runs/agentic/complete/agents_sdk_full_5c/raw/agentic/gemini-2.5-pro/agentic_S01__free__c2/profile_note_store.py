import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, Any

_mongo_client = None

def get_mongo_client():
    """Initializes and returns a MongoClient connected to MongoDB Atlas."""
    global _mongo_client
    if _mongo_client:
        return _mongo_client

    atlas_uri = os.getenv("MONGO_ATLAS_URI")
    if not atlas_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")
    
    # Create a new client and connect to the server
    # The URI must point to a *.mongodb.net domain for Atlas
    _mongo_client = MongoClient(atlas_uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        _mongo_client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(e)
        raise e

    return _mongo_client

def store_onboarding_note(user_id: str, note_data: Dict[str, Any]):
    """
    Persists a note related to a user's onboarding in a MongoDB collection.
    
    Args:
        user_id: The unique identifier for the user.
        note_data: A dictionary containing the note's content and metadata.
    """
    client = get_mongo_client()
    db = client.get_database("onboarding_db")
    notes_collection = db.get_collection("profile_notes")
    
    document = {
        "userId": user_id,
        **note_data
    }
    
    result = notes_collection.insert_one(document)
    return result.inserted_id
