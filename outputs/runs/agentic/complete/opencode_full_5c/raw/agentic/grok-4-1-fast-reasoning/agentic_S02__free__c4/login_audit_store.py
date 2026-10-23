import pymongo
import os
from datetime import datetime
from identity_models import AuditEvent


def persist_federated_login_audit_records(event: AuditEvent) -> None:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["identity_db"]
    collection = db["login_audits"]
    audit_doc = event.to_dict()
    audit_doc["persisted_at"] = datetime.utcnow().isoformat()
    collection.insert_one(audit_doc)
