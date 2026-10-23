import os
import boto3
from botocore.exceptions import ClientError
import uuid


def store_audit_record(record: dict):
    """Persists a message processing record in Amazon DynamoDB."""
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION_NAME", "us-east-1"),
    )

    table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    table = dynamodb.Table(table_name)

    # Ensure a unique ID for the audit record
    if "audit_id" not in record:
        record["audit_id"] = str(uuid.uuid4())

    try:
        table.put_item(Item=record)
        return record["audit_id"]
    except ClientError as e:
        # Handle potential errors, e.g., validation exceptions
        print(f"Error storing audit record: {e.response['Error']['Message']}")
        return None
