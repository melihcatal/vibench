import os
import json
from datetime import datetime
from messaging_models import normalize_request

# Provider: Amazon DynamoDB (example) for persisted message audit records
import boto3
from boto3.dynamodb.conditions import Attr

ddb = boto3.resource("dynamodb")
TABLE_NAME = os.getenv("MESSAGE_AUDIT_TABLE")
if not TABLE_NAME:
    raise RuntimeError("Set MESSAGE_AUDIT_TABLE environment variable")

table = ddb.Table(TABLE_NAME)


def store_message_audit(message_id: str, payload: dict, status: str, error: str = None):
    """Persist a processed message record for later lookup.

    The record schema includes:
        - id (partition key)
        - status (e.g., delivered, dead_letter)
        - timestamp (ISO string)
        - payload (JSON map)
        - error (optional description if failed)
    """
    now_iso = datetime.utcnow().isoformat()
    item = {
        "id": message_id,
        "status": status,
        "timestamp": now_iso,
        "payload": normalize_request(payload),
    }
    if error:
        item["error"] = error
    table.put_item(Item=item)
    print(f"Stored audit record for {message_id} with status {status} at {now_iso}")


if __name__ == "__main__":
    # Demo: insert a sample record
    sample_id = "audit_demo_001"
    sample_payload = {"orderId": "12345", "customer": "John Doe"}
    store_message_audit(sample_id, sample_payload, status="delivered")
