import os
import time
import uuid
from messaging_client import get_dynamodb_client
from messaging_models import AuditRecord

def store_audit_record(table_name: str, record: AuditRecord) -> dict:
    dynamodb_client = get_dynamodb_client()
    
    item = record.to_dict()
    # DynamoDB doesn't allow None values in items, filter them out.
    item_filtered = {k: v for k, v in item.items() if v is not None}

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item={k: {'S': str(v) if not isinstance(v, (dict, list)) else json.dumps(v)} for k, v in item_filtered.items()}
    )
    return response
