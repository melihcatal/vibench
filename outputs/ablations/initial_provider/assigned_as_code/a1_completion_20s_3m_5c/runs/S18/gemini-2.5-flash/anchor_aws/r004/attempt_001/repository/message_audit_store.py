import json
import os
import datetime

from messaging_client import get_dynamodb_client

def persist_message_record(message_id: str, payload: dict, processing_status: str, table_name: str = None, region_name: str = None):
    dynamodb_client = get_dynamodb_client(region_name)
    table_name = table_name or os.environ.get("DYNAMODB_AUDIT_TABLE_NAME")
    if not table_name:
        raise ValueError("DynamoDB table name must be provided or set in environment variables.")

    timestamp = datetime.datetime.utcnow().isoformat()

    item = {
        'message_id': {'S': message_id},
        'timestamp': {'S': timestamp},
        'payload': {'S': json.dumps(payload)},
        'processing_status': {'S': processing_status}
    }

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )
    
    return {"status": "Message record persisted", "message_id": message_id, "dynamodb_response_metadata": response["ResponseMetadata"]}
