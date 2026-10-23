import os
import pymongo
from typing import Dict, Any
from .identity_models import AuditEvent

MONGODB_URI = os.getenv('MONGODB_ATLAS_URI')
if not MONGODB_URI:
    raise ValueError('MONGODB_ATLAS_URI environment variable required')

client = pymongo.MongoClient(MONGODB_URI)
db = client['federated_login']
audits_collection = db['audit_events']

def store_audit_record(event: AuditEvent | Dict[str, Any]):
    audits_collection.insert_one(asdict(event) if hasattr(event, 'asdict') else event)
