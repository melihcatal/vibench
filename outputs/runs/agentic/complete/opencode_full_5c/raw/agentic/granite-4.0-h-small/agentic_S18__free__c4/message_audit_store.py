import json
from datetime import datetime
from database import (
    DBClient,
)  # assume a concrete database SDK (e.g., DynamoDB, PostgreSQL, etc.)
from messaging_models import MessagePayload, normalize_payload


def store_message_audit(payload: MessagePayload, status: str):
    """Persist a processed message record for later lookup.

    Args:
        payload (MessagePayload): Normalized message.
        status (str): Processing outcome ('success', 'retry', 'failure').
    """
    db = DBClient()  # concrete provider SDK (provider identifier in import)
    audit_record = {
        "message_id": payload.attributes.get("message_id") or str(uuid.uuid4()),
        "data": payload.data,
        "attributes": payload.attributes,
        "status": status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    # Simple upsert / insert logic (depends on DB type)
    db.insert("message_audit", audit_record)
    print(f"Stored audit record for message {audit_record['message_id']}")


if __name__ == "__main__":
    # Demo
    sample = {"key": "value"}
    msg = normalize_payload({"data": sample, "attributes": {"message_id": "demo-123"}})
    store_message_audit(msg, "success")
