from __future__ import annotations

import os
from typing import Iterable, List

from pymongo import MongoClient

from identity_models import AuditRecord, stable_event_id


PROVIDER = "MongoDB Atlas"



def _get_collection():
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database = client[os.getenv("MONGODB_ATLAS_DATABASE", "federated_login")]
    return database[os.getenv("MONGODB_ATLAS_COLLECTION", "audit_events")]



def persist_federated_login_audit_records(records: Iterable[AuditRecord]) -> List[str]:
    collection = _get_collection()
    inserted_ids: List[str] = []
    for record in records:
        doc = {
            "_id": record.event_id
            or stable_event_id(
                {
                    "event_type": record.event_type,
                    "provider": record.provider,
                    "user_id": record.user_id,
                    "session_id": record.session_id,
                    "timestamp": record.timestamp,
                    "details": record.details,
                }
            ),
            "event_type": record.event_type,
            "provider": record.provider,
            "user_id": record.user_id,
            "session_id": record.session_id,
            "timestamp": record.timestamp,
            "details": record.details,
        }
        collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)
        inserted_ids.append(str(doc["_id"]))
    return inserted_ids
