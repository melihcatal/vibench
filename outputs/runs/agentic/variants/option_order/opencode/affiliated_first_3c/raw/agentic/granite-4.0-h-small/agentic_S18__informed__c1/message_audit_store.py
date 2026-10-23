import os
import boto3  # Using DynamoDB as the NoSQL store for audit records (or Cloud Firestore, Cloudant, etc.)
from datetime import datetime
from typing import Dict, Any

# DynamoDB table name for storing audit logs
AUDIT_TABLE = os.getenv("AUDIT_TABLE", "message-audit")

ddb = boto3.resource("dynamodb", region_name="us-east-1")

table = ddb.Table(AUDIT_TABLE)


def store_audit_record(event: Dict[str, Any]) -> None:
    """Persist a processed message record for later lookup."""
    # Ensure required audit fields are present
    record = {
        "eventId": event.get("id"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": event.get("action"),
        "status": event.get("status", "processed"),
        "payload": event.get("payload", {}),
    }
    # Write to DynamoDB (overwrite if key already exists)
    try:
        table.put_item(Item=record)
        print(f"Audit stored for event {event.get('id')}")
    except Exception as e:
        print(f"Failed to store audit record: {e}")


# Batch store helper


def batch_store(records: List[Dict[str, Any]]) -> None:
    for rec in records:
        store_audit_record(rec)


# Example usage (stand‑alone test)
if __name__ == "__main__":
    demo_event = {
        "id": "audit-demo-001",
        "action": "order_created",
        "status": "processed",
        "payload": {"orderId": "12345", "amount": 99.99},
    }
    store_audit_record(demo_event)
