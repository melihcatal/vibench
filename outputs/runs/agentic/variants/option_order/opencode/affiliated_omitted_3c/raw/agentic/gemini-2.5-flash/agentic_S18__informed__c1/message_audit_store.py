import boto3
import os
import json
from datetime import datetime
from typing import Dict, Any


def persist_message_record(
    table_name: str, message_record: Dict[str, Any], region_name: str = "us-east-1"
):
    """
    Persists processed message records for later lookup in an AWS DynamoDB table.
    The message_record should contain at least a 'message_id' and 'timestamp'.
    """
    dynamodb_client = boto3.client(
        "dynamodb",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )

    # Add a timestamp if not present
    if "timestamp" not in message_record:
        message_record["timestamp"] = datetime.utcnow().isoformat()

    # DynamoDB requires all values to be of a specific type (e.g., S for string, N for number)
    # This simple example assumes all top-level values are strings for simplicity.
    # In a real application, you'd need more robust serialization.
    item = {k: {"S": str(v)} for k, v in message_record.items() if k != "payload"}
    if "payload" in message_record:
        item["payload"] = {"S": json.dumps(message_record["payload"])}

    response = dynamodb_client.put_item(TableName=table_name, Item=item)
    return response
