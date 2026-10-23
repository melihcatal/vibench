import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any

def get_dynamodb_table():
    """Initializes a boto3 DynamoDB table resource."""
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_AUDIT_TABLE environment variable not set.")
    
    # The AWS region, access key, and secret key are expected to be configured
    # via environment variables (AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # or an IAM role.
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table_name)

def store_audit_event(event: Dict[str, Any]) -> bool:
    """
    Persists a federated login audit event to Amazon DynamoDB.

    Args:
        event: A dictionary representing the audit event. Must include a primary key.

    Returns:
        True if the item was stored successfully, False otherwise.
    """
    try:
        table = get_dynamodb_table()
        response = table.put_item(Item=event)
        return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200
    except ClientError as e:
        print(f"Error storing audit event in DynamoDB: {e}")
        return False
