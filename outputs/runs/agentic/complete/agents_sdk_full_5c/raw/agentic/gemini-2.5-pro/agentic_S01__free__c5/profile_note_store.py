import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from typing import Dict, Any, Optional

def store_onboarding_note(user_id: str, note_data: Dict[str, Any]) -> Optional[str]:
    """
    Persists an onboarding note or support metadata in a MongoDB Atlas collection.
    
    The connection string should be set in the MONGODB_ATLAS_URI environment variable.
    Example: mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")
        
    client = MongoClient(uri, server_api=ServerApi('1'))
    
    try:
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(e)
        return None

    db = client.user_profiles
    notes_collection = db.onboarding_notes
    
    document_to_insert = {"user_id": user_id, **note_data}
    
    result = notes_collection.insert_one(document_to_insert)
    
    return str(result.inserted_id) if result.inserted_id else None
