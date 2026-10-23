# login_audit_store.py
# LATER-STEP: Persists federated‑login audit records in a managed document store (e.g., DynamoDB, Firestore, Azure Cosmos DB)

# This module provides a thin wrapper over a provider's managed document store SDK.
# The concrete client class is imported from a provider‑specific package, making
# the integration easy to swap (e.g., AWS SDK for DynamoDB vs. Google Firestore vs. Azure Cosmos SDK).

# Example using AWS DynamoDB via boto3 (replace with the appropriate provider SDK)
import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any

# AWS DynamoDB dependency – will be present in the environment where the service runs
import boto3  # type: ignore

# Configure the client once per process
# Adjust `resource_name` or `endpoint_url` when using a different provider
ddb_table_name = os.getenv("AUDIT_TABLE_NAME", "login-audit")
region = os.getenv("AWS_REGION", "us-east-1")

ddb_client = boto3.client("dynamodb", region_name=region)

table = boto3.resource("dynamodb", region_name=region).Table(ddb_table_name)

# Expected audit schema fields (minimum required by other modules)
REQUIRED_FIELDS = {
    "event_id": str,
    "user_id": str,
    "timestamp": str,  # ISO‑8601 string
    "type": str,
    "details": dict,
}


def _validate(record: Dict[str, Any]) -> None:
    for key, expected_type in REQUIRED_FIELDS.items():
        if key not in record:
            raise ValueError(f"Missing required audit field: {key}")
        if not isinstance(record[key], expected_type):
            raise TypeError(
                f"Field '{key}' must be of type {expected_type.__name__}, got {type(record[key])}"
            )


def store_audit(
    event_type: str, user_id: str, details: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create an audit record, validate it, and write it to the managed store.
    Returns the saved record (including generated fields such as DynamoDB's PK).
    """
    record = {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": event_type,
        "details": details or {},
    }
    _validate(record)
    # Marshal to a format DynamoDB expects (DynamoDBAttribute format is handled by Table.put_item)
    ddb_client.put_item(TableName=ddb_table_name, Item=record)
    return record


# ---- Helper for reading recent records (for testing / admin UI) ----


def fetch_recent(limit: int = 20) -> List[Dict[str, Any]]:
    """Fetch the most recent audit records ordered by timestamp descending."""
    response = ddb_client.query(
        TableName=ddb_table_name,
        IndexName="timestamp-index",  # assume a GSI on timestamp for fast retrieval
        ScanIndexForward=False,  # descending order
        Limit=limit,
        ProjectionExpression="#t, #u, #ts, #id",
        ExpressionAttributeNames={
            "#t": "type",
            "#u": "user_id",
            "#ts": "timestamp",
            "#id": "event_id",
        },
    )
    return response.get("Items", [])


# ---- Example usage for local testing ----
if __name__ == "__main__":
    # Ensure a table exists before testing – in production this would be provisioned separately
    # Here we only run a quick demo if the environment is set up
    try:
        store_audit(
            event_type="login_success", user_id="u_123", details={"ip": "203.0.113.7"}
        )
        store_audit(
            event_type="code_exchange",
            user_id="u_123",
            details={"access_token": "tok_demo"},
        )
        print("Stored two demo audit events.")
        recents = fetch_recent(limit=5)
        print("Recent audit entries:")
        for r in recents:
            print(json.dumps(r, indent=2))
    except Exception as e:
        print("Audit store demo failed:", e)
