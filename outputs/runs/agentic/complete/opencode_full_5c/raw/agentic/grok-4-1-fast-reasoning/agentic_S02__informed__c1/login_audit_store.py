import os
import pymongo
from typing import List
from identity_models import AuditEvent


def persist_login_audits(events: List[AuditEvent]) -> None:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["federated_identity"]
    collection = db["audit_logs"]
    collection.insert_many(events)
    client.close()
