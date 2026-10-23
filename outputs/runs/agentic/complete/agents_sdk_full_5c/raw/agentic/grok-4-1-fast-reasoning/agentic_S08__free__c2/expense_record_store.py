import os
import pymongo
import uuid
from typing import Dict, Any, Optional

def store_expense_record(normalized: Dict[str, Any], record_id: Optional[str] = None) -> str:
    uri = os.getenv('MONGODB_ATLAS_URI')
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI not set")
    client = pymongo.MongoClient(uri)
    db = client['expenses']
    collection = db['records']
    if record_id is None:
        record_id = str(uuid.uuid4())
    normalized['_id'] = record_id
    result = collection.insert_one(normalized)
    client.close()
    return str(result.inserted_id)
