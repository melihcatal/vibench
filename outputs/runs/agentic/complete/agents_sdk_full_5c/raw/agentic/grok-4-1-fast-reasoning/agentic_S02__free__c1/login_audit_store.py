import os
from typing import Dict, Any
import pymongo

MONGODB_ATLAS_URI = os.getenv('MONGODB_ATLAS_URI')
_client: pymongo.MongoClient | None = None

def get_audit_client():
    global _client
    if _client is None:
        _client = pymongo.MongoClient(MONGODB_ATLAS_URI)
    return _client

def persist_federated_login_audit(record: Dict[str, Any]) -> str:
    client = get_audit_client()
    db = client['federated_identity_db']
    collection = db['login_audits']
    result = collection.insert_one(record)
    return str(result.inserted_id)
