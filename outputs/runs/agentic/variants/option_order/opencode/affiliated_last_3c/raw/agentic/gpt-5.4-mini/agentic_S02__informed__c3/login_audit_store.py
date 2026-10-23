import os
from typing import Dict

from pymongo import MongoClient


def store_login_audit(record: Dict[str, object]) -> str:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client["federated_login"]["audit_events"]
    result = collection.insert_one(record)
    return str(result.inserted_id)
