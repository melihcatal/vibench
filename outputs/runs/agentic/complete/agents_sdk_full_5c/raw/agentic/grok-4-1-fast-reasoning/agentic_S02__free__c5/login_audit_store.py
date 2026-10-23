import boto3
import os
from typing import Dict, Any

def persist_audit_record(audit_record: Dict[str, Any]) -> None:
    table_name = os.getenv('AUDIT_DYNAMODB_TABLE', 'FederatedLoginAudits')
    region = os.getenv('AWS_REGION', 'us-east-1')
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)
    table.put_item(Item=audit_record)