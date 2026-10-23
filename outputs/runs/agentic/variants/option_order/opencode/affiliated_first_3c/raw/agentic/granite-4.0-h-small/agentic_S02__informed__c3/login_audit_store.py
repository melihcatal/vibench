import os
import json
from datetime import datetime
from identity_models import PersistedAuditRecord
from pymongo import MongoClient

# MongoDB Atlas configuration (replace with your own URI & DB name)
MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
MONGO_DB_NAME = os.getenv("MONGODB_ATLAS_DB_NAME", "login_audit")

# Initialize a persistent NoSQL store
client = MongoClient(MONGO_URI)
DB = client[MONGO_DB_NAME]
COLLECTION = DB["audit_events"]


def store_audit_record(record: PersistedAuditRecord):
    """Persist an audit record document in MongoDB."""
    payload = record._asdict()
    COLLECTION.insert_one(payload)


# Example usage for demonstration
if __name__ == "__main__":
    demo_record = PersistedAuditRecord(
        user_sub="u_demo",
        event_type="login_success",
        details={"method": "code", "provider": "ibm_appid"},
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
    store_audit_record(demo_record)
    print("Demo audit record stored in MongoDB.")
