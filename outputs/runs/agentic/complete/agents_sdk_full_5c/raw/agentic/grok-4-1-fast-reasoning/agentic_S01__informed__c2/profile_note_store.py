import os
import pymongo
from datetime import datetime
from typing import Dict, Any

def profile_note_store(user_id: str, notes: Dict[str, Any]) -> None:
    """
    Persist onboarding notes and support metadata in a managed document store
    """
    uri = os.getenv('MONGODB_ATLAS_URI')
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI required")
    
    mongo_client = None
    try:
        mongo_client = pymongo.MongoClient(uri)
        db = mongo_client['identity_app']
        collection = db['profile_notes']
        
        update_doc = {
            'user_id': user_id,
            'notes': notes,
            'updated_at': datetime.utcnow()
        }
        
        result = collection.replace_one(
            {'user_id': user_id},
            update_doc,
            upsert=True
        )
    finally:
        if mongo_client:
            mongo_client.close()