import os
from datetime import datetime, timezone

from pymongo import MongoClient


client = MongoClient(os.environ['MONGODB_ATLAS_URI'])
collection = client['federated_login']['audit_events']


def store_audit_record(record: dict) -> str:
    payload = {**record, 'stored_at': datetime.now(timezone.utc)}
    result = collection.insert_one(payload)
    return str(result.inserted_id)
