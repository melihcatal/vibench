import os
import time
from typing import Dict
import boto3

# DynamoDB credentials via AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
TABLE_NAME = os.getenv("DYNAMO_AUDIT_TABLE")
if not TABLE_NAME:
    raise RuntimeError("DYNAMO_AUDIT_TABLE environment variable not set")
ddb = boto3.resource('dynamodb')
table = ddb.Table(TABLE_NAME)

def audit_message(message_id: str, event: Dict, outcome: str, error_detail: str = None) -> None:
    """Persist an audit record for a processed message in DynamoDB.

    Each record contains:
      - message_id (string, primary key)
      - received_at (ISO 8601 timestamp)
      - payload (stringified JSON)
      - outcome (e.g., 'processed', 'dead_letter', 'failed')
      - error_detail (optional string)
      - audit_timestamp (epoch seconds)
    """
    record = {
        "message_id": message_id,
        "received_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "payload": json.dumps(event),
        "outcome": outcome,
        "error_detail": error_detail,
        "audit_timestamp": int(time.time()),
    }
    table.put_item(Item=record)
    print(f"Audited record for {message_id}")


def query_failed_messages(limit: int = 10) -> list[Dict]:
    """Retrieve the most recent failed messages (outcome='failed')."""
    response = table.query(
        KeyConditionExpression='outcome = :val',
        ExpressionAttributeValues={":val": "failed"},
        ScanIndexForward=False,   # newest first
        Limit=limit,
    )
    return [item for item in response['Items']]
