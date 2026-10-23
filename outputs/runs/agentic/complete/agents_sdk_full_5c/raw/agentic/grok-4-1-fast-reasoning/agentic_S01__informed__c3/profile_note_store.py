import os
from typing import Dict, Any
from datetime import datetime
import pymongo

def store_profile_notes(user_id: str, notes: Dict[str, Any]) -&gt; bool:
    uri = os.getenv('MONGODB_ATLAS_URI')
    client = pymongo.MongoClient(uri)
    db = client['onboarding_db']
    collection = db['profile_notes']
    result = collection.update_one(
        {'user_id': user_id},
        {'$set': {
            'notes': notes,
            'updated_at': datetime.utcnow(),
        }},
        upsert=True
    )
    client.close()
    return result.acknowledged