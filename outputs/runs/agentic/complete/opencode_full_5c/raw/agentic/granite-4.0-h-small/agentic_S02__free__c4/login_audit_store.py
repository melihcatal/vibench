import json
from datetime import datetime
from typing import Any, Dict

AuditRecord = Dict[str, Any]

# In a real deployment this would be a managed document store (e.g., Amazon DocumentDB, DynamoDB, or a MongoDB Atlas cluster).
# For the purpose of this example we write JSON files to a local "audit_store" directory.

AUDIT_STORE_DIR = "audit_store"

# Ensure the directory exists (in real code, use os.makedirs with exist_ok=True)
# For this script we assume the directory is already present or the user will create it.


def store_audit_record(record: AuditRecord) -> str:
    """Persist a federated‑login audit record to the document store.

    The record must contain at least: event_type, timestamp, user_id.
    Returns the generated file path (or identifier) for the persisted record.
    """
    if not isinstance(record, dict):
        raise ValueError("Audit record must be a dict")
    # Simple filename based on timestamp
    safe_id = datetime.utcfromtimestamp(record.get("timestamp", 0)).strftime(
        "%Y%m%dT%H%M%S.%fZ"
    )
    filepath = f"{AUDIT_STORE_DIR}/audit_{safe_id}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return filepath


if __name__ == "__main__":
    # Example usage
    example_record = {
        "event_type": "login_success",
        "timestamp": datetime.utcnow().timestamp(),
        "user_id": "user_12345",
        "notes": "PKCE flow completed successfully",
    }
    path = store_audit_record(example_record)
    print("Persisted audit record to", path)
