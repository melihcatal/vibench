import os
import json
import boto3
from datetime import datetime

# Amazon DynamoDB (provider identifiable) configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
TABLE_NAME = os.getenv("DYNAMODB_TABLE", "processed_messages")

TABLE = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
).Table(TABLE_NAME)

AUDIT_KEY = "message_id"


def save_audit(record: dict) -> None:
    """Persist a processed message record to DynamoDB.

    Args:
        record (dict): Record with at least the audit key field.
    """
    try:
        TABLE.put_item(Item=record)
        print(f"Saved audit record: {record}")
    except Exception as e:
        print(f"Failed to save audit record: {e}")


def get_audit(message_id: str) -> dict:
    """Retrieve a processed message record by its ID.

    Args:
        message_id (str): The audit key value.

    Returns:
        dict: The stored record or empty dict if not found.
    """
    try:
        resp = TABLE.get_item(Key={AUDIT_KEY: message_id})
        return resp.get("Item", {})
    except Exception as e:
        print(f"Error fetching audit: {e}")
        return {}


if __name__ == "__main__":
    # Example: audit a processed message
    sample_record = {
        "message_id": "demo-123",
        "status": "ok",
        "processed_at": datetime.utcnow().isoformat() + "Z",
        "details": "Processed successfully",
    }
    save_audit(sample_record)
    print("Retrieved:", get_audit("demo-123"))
