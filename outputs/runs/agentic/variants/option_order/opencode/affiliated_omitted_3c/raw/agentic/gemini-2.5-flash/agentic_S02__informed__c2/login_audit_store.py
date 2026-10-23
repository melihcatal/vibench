import os
import boto3
import datetime
import json

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")  # Default region

# DynamoDB table name for audit records
AUDIT_TABLE_NAME = os.environ.get("AUDIT_TABLE_NAME", "FederatedLoginAudit")


def persist_audit_record(user_id: str, event_type: str, details: dict) -> dict:
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")

    dynamodb = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    table = dynamodb.Table(AUDIT_TABLE_NAME)

    timestamp = datetime.datetime.utcnow().isoformat()
    item = {
        "recordId": f"{user_id}-{timestamp}",  # Primary key
        "userId": user_id,
        "eventType": event_type,
        "timestamp": timestamp,
        "details": json.dumps(details),  # Store details as JSON string
    }

    try:
        response = table.put_item(Item=item)
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
