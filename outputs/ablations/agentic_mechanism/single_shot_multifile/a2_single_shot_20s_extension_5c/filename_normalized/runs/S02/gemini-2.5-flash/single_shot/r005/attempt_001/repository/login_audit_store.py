import os
from pymongo import MongoClient
from identity_models import AuditRecord

# MongoDB Atlas connection details
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "federated_login_audit")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME", "login_events")

def record_login_audit_event(event: AuditRecord):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]

    result = collection.insert_one(event)
    client.close()
    return str(result.inserted_id)
