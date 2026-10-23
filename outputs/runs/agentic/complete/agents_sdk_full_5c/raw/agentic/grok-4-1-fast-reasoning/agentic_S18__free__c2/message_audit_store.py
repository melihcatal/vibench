import boto3
import os
from typing import Dict, Any

def message_audit_store(record: Dict[str, Any]) -> str:
    """
    Persist processed message records for later lookup
    """
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    table_name = os.getenv('AUDIT_TABLE_NAME')
    table = dynamodb.Table(table_name)
    table.put_item(Item=record)
    return record.get('message_id', 'unknown')