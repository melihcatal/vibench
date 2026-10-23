from __future__ import annotations

import os
from typing import Iterable

from pymongo import MongoClient

from identity_models import AuditRecord, model_dump


MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_ATLAS_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_ATLAS_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


def _collection():
    client = MongoClient(os.environ[MONGODB_ATLAS_URI_ENV])
    database = os.getenv(MONGODB_ATLAS_DB_ENV, "federated_login")
    collection = os.getenv(MONGODB_ATLAS_COLLECTION_ENV, "audit_records")
    return client[database][collection]


def store_audit_record(record: AuditRecord) -> str:
    collection = _collection()
    document = model_dump(record)
    document["_id"] = record.record_id
    collection.replace_one({"_id": record.record_id}, document, upsert=True)
    return record.record_id


def store_audit_records(records: Iterable[AuditRecord]) -> int:
    collection = _collection()
    count = 0
    for record in records:
        document = model_dump(record)
        document["_id"] = record.record_id
        collection.replace_one({"_id": record.record_id}, document, upsert=True)
        count += 1
    return count
