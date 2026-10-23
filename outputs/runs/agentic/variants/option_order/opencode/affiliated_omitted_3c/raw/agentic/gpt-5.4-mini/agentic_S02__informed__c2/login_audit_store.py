import os
from typing import Any, Dict

import boto3

AUDIT_TABLE_NAME = os.environ.get('AUDIT_TABLE_NAME', 'federated-login-audit')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')


def store_audit_record(record: Dict[str, Any]) -> Dict[str, Any]:
    table = boto3.resource('dynamodb', region_name=AWS_REGION).Table(AUDIT_TABLE_NAME)
    table.put_item(Item=record)
    return record
