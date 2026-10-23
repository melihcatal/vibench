from __future__ import annotations

import os
from typing import Iterable, List

from pymongo import MongoClient

from identity_models import AuditEvent, audit_event_document


def store_audit_events(events: Iterable[AuditEvent]) -> List[str]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.environ.get("MONGODB_ATLAS_DATABASE", "federated_login")
    collection_name = os.environ.get("MONGODB_ATLAS_COLLECTION", "audit_events")
    collection = client[database_name][collection_name]
    documents = [audit_event_document(event) for event in events]
    if not documents:
        return []
    result = collection.insert_many(documents, ordered=True)
    return [str(item) for item in result.inserted_ids]
