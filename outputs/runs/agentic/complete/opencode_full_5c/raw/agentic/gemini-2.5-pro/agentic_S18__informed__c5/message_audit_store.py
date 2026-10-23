import boto3
import os
from decimal import Decimal
import json


def store_message_audit(record: dict):
    """Persists a processed message record to Amazon DynamoDB."""
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE", "message_audit")
    table = dynamodb.Table(table_name)

    # Convert floats to Decimals for DynamoDB
    item_decimal = json.loads(json.dumps(record), parse_float=Decimal)

    response = table.put_item(Item=item_decimal)

    return response
