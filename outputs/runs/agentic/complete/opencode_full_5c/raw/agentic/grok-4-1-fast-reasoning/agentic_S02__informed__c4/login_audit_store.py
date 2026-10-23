from typing import List
import pymongo
import os
from dataclasses import asdict
from identity_models import AuditEvent


def store_audit_events(
    events: List[AuditEvent],
    database: str = "identity_audit",
    collection: str = "login_events",
):
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI not set")
    client = pymongo.MongoClient(uri)
    db = client[database]
    col = db[collection]
    if events:
        inserted = col.insert_many([asdict(event) for event in events])
        print(f"Inserted {len(inserted.inserted_ids)} audit events into MongoDB Atlas")
    else:
        print("No events to store")
