# message_audit_store.py
# LATER-STEP: Persist processed message details for later retrieval

import os
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any
from messaging_models import Event, ErrorResponse

# Choose a NoSQL store based on env variable
STORE_TYPE = os.getenv("AUDIT_STORE_PROVIDER", "dynamodb")

# Stub implementations for demonstration purposes
if STORE_TYPE == "dynamodb":
    # Placeholder DynamoDB client using boto3
    from .audit_providers import dynamodb_audit as audit_provider
elif STORE_TYPE == "mongodb":
    # Placeholder MongoDB client using pymongo
    from .audit_providers import mongodb_audit as audit_provider
else:
    # Fallback in-memory store for testing
    _store: Dict[str, Any] = {}

    class InMemoryAudit:
        def store(self, record: Dict[str, Any]) -> None:
            uid = record.get("eventId") or datetime.utcnow().isoformat()
            _store[uid] = record

        def retrieve(self, evt_id: str) -> Optional[Dict[str, Any]]:
            return _store.get(evt_id)

    audit_provider = InMemoryAudit()


class AuditRecord(BaseModel):
    """Schema for an entry stored in the audit store."""

    eventId: str = Field(..., description="Original event identifier")
    status: str = Field(..., description="Processing result status")
    payload: Dict[str, Any] = Field(
        ..., description="Normalized payload, may include error info"
    )
    processedAt: str = Field(
        default_factory=datetime.utcnow, description="UTC timestamp when stored"
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "eventId": self.eventId,
            "status": self.status,
            "payload": self.payload,
            "processedAt": str(self.processedAt),
        }


def audit_event(
    event: Event, status: str, error: Optional[ErrorResponse] = None
) -> None:
    """Persist a summary of the message processing attempt."""
    record = {
        "eventId": event.event_id,
        "status": status,
        "payload": event.dict()
        if status == "success"
        else (error.dict() if error else {}),
    }
    audit_record = AuditRecord(**record)
    audit_provider.store(audit_record.dict())
    print(f"Audit stored for event {event.event_id} with status {status}")


def lookup_audit(event_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve a stored audit record by its eventId."""
    record = audit_provider.retrieve(event_id)
    return record


# ---- Provider skeletons ------------------------------------------------------
# Replace these skeletons with actual SDK usage in production.
# Example DynamoDB skeleton (requires boto3):
# class dynamodb_audit:
#     def store(self, record: Dict[str, Any]) -> None:
#         import boto3, json
#         client = boto3.resource('dynamodb')
#         table = client.Table(os.getenv('DDB_TABLE'))
#         table.put_item(Item=record)
#
# Example MongoDB skeleton (requires pymongo):
# class mongodb_audit:
#     def store(self, record: Dict[str, Any]) -> None:
#         import pymongo
#         client = pymongo.MongoClient(os.getenv('MONGO_URI'))
#         db = client[os.getenv('MONGO_DB')]
#         coll = db[os.getenv('MONGO_COLLECTION')]
#         coll.insert_one(record)
#
# Example InMemoryAudit (already defined above)

if __name__ == "__main__":
    # Demo with in-memory store
    evt = Event(
        event_id="audit-demo-001",
        data={"text": "Sample"},
        timestamp="2025-08-01T12:00:00Z",
    )
    audit_event(evt, status="success")
    lookup = lookup_audit("audit-demo-001")
    print("Audit lookup result:", lookup)
