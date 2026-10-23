import pymongo
from pymongo.errors import PyMongoError
import os
from typing import Dict, Any
from messaging_models import AuditRecord

MONGODB_ATLAS_URI = os.getenv('MONGODB_ATLAS_URI')
mongo_client = pymongo.MongoClient(MONGODB_ATLAS_URI)
db = mongo_client['message_audit']
collection = db['processed_messages']

def persist_message_audit(record: Dict[str, Any]) -> str:
    """
    Persists processed message records to MongoDB Atlas for later lookup.
    """
    try:
        audit_record = AuditRecord(**record)
        result = collection.insert_one(audit_record.model_dump())
        return str(result.inserted_id)
    except PyMongoError as e:
        raise Exception(f"Failed to store audit record: {e}")
