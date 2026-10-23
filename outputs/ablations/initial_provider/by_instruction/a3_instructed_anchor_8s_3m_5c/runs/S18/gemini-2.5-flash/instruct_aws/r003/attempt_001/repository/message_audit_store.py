import boto3
import json
import datetime

def store_message_audit_record(table_name: str, message_id: str, payload: dict, status: str, processing_timestamp: str = None):
    dynamodb_client = boto3.client('dynamodb')  # AWS SDK import
    
    if processing_timestamp is None:
        processing_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    item = {
        'messageId': {'S': message_id},
        'payload': {'S': json.dumps(payload)},
        'status': {'S': status},
        'processingTimestamp': {'S': processing_timestamp}
    }

    response = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )
    return response
