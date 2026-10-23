from pymongo import MongoClient
from identity_client import IdentityClientConfig
from identity_models import AuditRecord
from datetime import datetime
import uuid


def store_audit_record(user_id: str, event_type: str, ip_address: str, details: dict):
    config = IdentityClientConfig()
    client = MongoClient(config.MONGO_ATLAS_URI)
    db = client.get_database("audit_logs")
    collection = db.get_collection("logins")

    audit_record = AuditRecord(
        event_id=str(uuid.uuid4()),
        user_id=user_id,
        event_type=event_type,
        timestamp=datetime.utcnow().isoformat(),
        ip_address=ip_address,
        details=details,
    )

    collection.insert_one(audit_record.dict())
    client.close()
