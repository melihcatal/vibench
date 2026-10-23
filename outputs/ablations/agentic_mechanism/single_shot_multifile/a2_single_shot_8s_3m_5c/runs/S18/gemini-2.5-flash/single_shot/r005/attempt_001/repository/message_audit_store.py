import os
import json
from datetime import datetime
from messaging_client import get_dynamodb_client
from messaging_models import ProcessedMessageRecord

def store_processed_message(record: ProcessedMessageRecord, table_name: str) -> dict:
    dynamodb_client = get_dynamodb_client()
    try:
        item = {
            'record_id': {'S': record.record_id},
            'original_message_id': {'S': record.original_message_id},
            'processed_timestamp': {'S': record.processed_timestamp},
            'processing_status': {'S': record.processing_status},
        }

        if record.summary is not None:
            item['summary'] = {'S': record.summary}
        if record.safety_check_result is not None:
            item['safety_check_result'] = {'S': json.dumps(record.safety_check_result)} 
        if record.translated_payload is not None:
            item['translated_payload'] = {'S': json.dumps(record.translated_payload)} 
        if record.original_payload is not None:
            item['original_payload'] = {'S': json.dumps(record.original_payload)} 

        response = dynamodb_client.put_item(
            TableName=table_name,
            Item=item
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to store processed message record in DynamoDB: {e}")
