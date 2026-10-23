import os
import json
import datetime
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import BotoCoreError, ClientError

# Managed NoSQL Document Store for audit records
# Using Amazon DynamoDB as the concrete managed store

dynamo = boto3.resource("dynamodb", region_name=os.getenv("AWS_REGION", "us-east-1"))
TABLE_NAME = os.getenv("AUDIT_TABLE_NAME", "federated-login-audit")


def ensure_audit_table():
    """Create the audit table if it does not exist.
    Expected schema:
        Partition key: session_id (String)
        Sort key: event_timestamp (String, ISO8601)
    Returns:
        boto3.Table: The DynamoDB table object.
    """
    try:
        table = dynamo.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "session_id", "KeyType": "HASH"},
                {"AttributeName": "event_timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "session_id", "AttributeType": "S"},
                {"AttributeName": "event_timestamp", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            BillingMode="PROVISIONED",  # change to PAY_PER_REQUEST if needed
        )
        table.wait_until_exists()
    except ClientError as e:
        # Table already exists or other non-fatal error
        if e.response["Error"]["Code"] != "ResourceInUseException":
            raise
    return dynamo.Table(TABLE_NAME)


def store_audit_event(event: dict):
    """Persist a single federated-login audit event.
    The function ensures the table exists and writes the record.
    Args:
        event (dict): Must contain at least 'session_id' and 'event_timestamp'.
    """
    table = ensure_audit_table()
    try:
        response = table.put_item(Item=event)
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to store audit event: {e}")
    return response


# Example usage (for local testing):
# audit = {
#     "session_id": "abc123",
#     "event_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
#     "event_type": "login_success",
#     "provider": "cognito",
#     "user_id": "user-xyz",
# }
# store_audit_event(audit)
