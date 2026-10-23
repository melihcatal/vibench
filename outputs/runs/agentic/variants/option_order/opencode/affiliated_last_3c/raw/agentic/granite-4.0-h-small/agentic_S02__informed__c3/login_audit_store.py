import os
import json
from datetime import datetime
from typing import TypedDict
from identity_client import IdentityClient, DocumentStoreClient
from identity_models import AuditRecord, AuditRecordMetadata

# Example managed store: MongoDB Atlas using pymongo
MONGO_ATLAS_URI = os.getenv("MONGO_ATLAS_URI")


class StoredAudit(TypedDict):
    _id: str
    record: AuditRecord
    stored_at: datetime


# Initialise a persistent client
store_client = DocumentStoreClient(MONGO_ATLAS_URI)
COLLECTION_NAME = "federated_login_audit"


def persist_audit(record: AuditRecord) -> StoredAudit:
    """Persist a federated login audit record in the managed document store.
    Returns the stored document identifier and timestamp.
    """
    collection = store_client.get_collection(COLLECTION_NAME)
    now = datetime.utcnow()
    meta = AuditRecordMetadata(stored_at=now)
    full_record = AuditRecord(**{**record.dict(), "metadata": meta})
    result = collection.insert_one(full_record)
    return StoredAudit(
        _id=str(result.inserted_id),
        record=full_record,
        stored_at=now,
    )
