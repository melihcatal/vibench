import os
import boto3
import json
from datetime import datetime
from typing import Dict, Any

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AUDIT_TABLE_NAME = os.environ.get("AUDIT_TABLE_NAME", "FederatedLoginAudit")

def persist_audit_record(audit_record: Dict[str, Any]):
    """
    Persists federated-login audit records in an AWS DynamoDB table.
    """
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(AUDIT_TABLE_NAME)

    try:
        # Add a timestamp if not already present
        if "timestamp" not in audit_record:
            audit_record["timestamp"] = int(datetime.now().timestamp() * 1000) # Milliseconds since epoch
        
        # DynamoDB requires all top-level items to be non-empty strings, numbers, or booleans
        # Convert any complex objects to JSON strings if they are not already handled
        item_to_put = audit_record.copy()
        for key, value in item_to_put.items():
            if isinstance(value, dict) or isinstance(value, list):
                item_to_put[key] = json.dumps(value)

        response = table.put_item(Item=item_to_put)
        print(f"Successfully persisted audit record with ID: {audit_record.get('id', 'N/A')}")
        return response
    except Exception as e:
        print(f"Error persisting audit record to DynamoDB: {e}")
        raise

if __name__ == "__main__":
    example_audit_record = {
        "id": "login-event-12345",
        "user_id": "testuser-123",
        "event_type": "LOGIN_SUCCESS",
        "provider": "Cognito",
        "ip_address": "192.168.1.1",
        "user_agent": "Mozilla/5.0",
        "details": {
            "session_id": "abc-123",
            "claims_received": {"email": "test@example.com"}
        }
    }

    try:
        response = persist_audit_record(example_audit_record)
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}")
