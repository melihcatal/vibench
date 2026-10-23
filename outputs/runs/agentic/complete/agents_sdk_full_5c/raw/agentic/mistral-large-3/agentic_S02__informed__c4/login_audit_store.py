import os
from pymongo import MongoClient
from identity_models import LoginAuditRecord

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")

client = MongoClient(MONGODB_ATLAS_URI)
db = client["federated_login"]
audit_collection = db["audit_records"]


def store_audit_record(record: LoginAuditRecord):
    audit_collection.insert_one(record.dict())