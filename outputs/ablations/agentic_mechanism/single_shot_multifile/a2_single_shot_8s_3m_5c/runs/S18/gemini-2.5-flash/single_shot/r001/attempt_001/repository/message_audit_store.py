import os
import json
from datetime import datetime
from typing import Dict, Any
from messaging_client import get_dynamodb_client
from messaging_models import AuditRecord

def persist_audit_record(record: AuditRecord, table_name: str):
    dynamodb_client = get_dynamodb_client()

    item_dict = {
        'message_id': {'S': record.message_id},
        'original_payload': {'S': json.dumps(record.original_payload)}
    }

    if record.processed_payload:
        item_dict['processed_payload'] = {'S': json.dumps(record.processed_payload)}
    if record.processing_summary:
        item_dict['processing_summary'] = {'S': record.processing_summary}
    if record.translation_status:
        item_dict['translation_status'] = {'S': record.translation_status}
    if record.safety_check_result:
        item_dict['safety_check_result'] = {'S': json.dumps(record.safety_check_result)}
    
    item_dict['timestamp'] = {'S': record.timestamp}

    try:
        response = dynamodb_client.put_item(
            TableName=table_name,
            Item=item_dict
        )
        return response
    except Exception as e:
        return {"error": str(e)}