from __future__ import annotations

from typing import Iterable

from pymongo import MongoClient

from identity_models import AuditRecord, to_dict

MONGODB_URI_ENV = "MONGODB_ATLAS_URI"


def persist_audit_records(records: Iterable[AuditRecord]) -> int:
    import os

    client = MongoClient(os.environ.get(MONGODB_URI_ENV, "mongodb://localhost:27017"))
    collection = client["federated_login"]["audit_records"]
    docs = [to_dict(record) for record in records]
    if docs:
        collection.insert_many(docs)
    return len(docs)
