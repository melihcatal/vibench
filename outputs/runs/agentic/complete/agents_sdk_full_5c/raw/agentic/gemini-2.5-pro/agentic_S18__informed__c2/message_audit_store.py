import os
import boto3
from botocore.exceptions import ClientError
import uuid
import time
from typing import Dict, Any

def store_audit_record(processed_message: Dict[str, Any]):
    """
    Persists a processed message record to Amazon DynamoDB for later lookup.

    Args:
        processed_message: A dictionary representing the message and its
                           processing outcome.
    """
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get("DYNAMODB_AUDIT_TABLE_NAME")
    if not table_name:
        raise ValueError("DYNAMODB_AUDIT_TABLE_NAME environment variable not set.")
        
    table = dynamodb.Table(table_name)
    
    # Enrich the record with audit-specific fields
    record = processed_message.copy()
    record['recordId'] = str(uuid.uuid4())
    record['processedAt'] = int(time.time())
    
    try:
        response = table.put_item(
           Item=record
        )
        print(f"Successfully stored audit record {record['recordId']} in DynamoDB.")
        return response
    except ClientError as e:
        print(f"Error persisting to DynamoDB: {e.response['Error']['Message']}")
        raise
