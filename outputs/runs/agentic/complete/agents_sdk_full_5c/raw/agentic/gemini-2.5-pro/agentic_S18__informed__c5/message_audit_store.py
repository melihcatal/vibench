import os
import boto3
from botocore.exceptions import ClientError
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_dynamodb_table():
    """Initializes and returns a DynamoDB table resource."""
    table_name = os.getenv("DYNAMODB_AUDIT_TABLE")
    if not table_name:
        raise ValueError("DYNAMODB_AUDIT_TABLE environment variable not set.")

    # Using default credential provider (e.g., IAM role, env vars)
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table_name)

def store_audit_record(record_id: str, data: Dict[str, Any]) -> bool:
    """
    Persists a processed message record to Amazon DynamoDB.

    Args:
        record_id: The unique identifier for the record (e.g., message ID).
        data: A dictionary containing the message data and processing results.

    Returns:
        True if the item was stored successfully, False otherwise.
    """
    table = get_dynamodb_table()
    
    item_to_store = {
        'recordId': record_id,
        'payload': data
    }

    try:
        response = table.put_item(Item=item_to_store)
        logger.info(f"Successfully stored audit record {record_id}.")
        # Check for successful HTTP status code
        return response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200
    except ClientError as e:
        logger.error(
            "Couldn't store audit record %s in table %s. Here's why: %s: %s",
            record_id,
            table.name,
            e.response['Error']['Code'],
            e.response['Error']['Message']
        )
        return False
