import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Dict, Any

def store_onboarding_note(user_id: str, note_data: Dict[str, Any]) -> str:
    """
    Persists a user's onboarding notes and metadata in MongoDB Atlas.

    Requires MONGO_ATLAS_URI environment variable.
    Example URI: mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
    """
    mongo_uri = os.environ.get("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable is not set.")

    try:
        client = MongoClient(mongo_uri)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure as e:
        raise Exception(f"Could not connect to MongoDB Atlas: {e}")

    try:
        db = client.get_default_database() # Or specify a db name: client['onboarding_db']
        notes_collection = db["profile_notes"]
        
        document_to_insert = {"user_id": user_id, **note_data}
        
        result = notes_collection.insert_one(document_to_insert)
        return str(result.inserted_id)
    except OperationFailure as e:
        raise Exception(f"An error occurred during a database operation: {e.details}")
    finally:
        client.close()
