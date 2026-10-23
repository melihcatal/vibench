import os
import boto3
import datetime
import json

from messaging_models import Message

def persist_message_record(message: Message, processing_status: str, audit_data: dict = None, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    table_name = config.get("dynamodb_table_name", os.environ.get("DYNAMODB_AUDIT_TABLE_NAME"))

    if not table_name:
        raise ValueError("DYNAMODB_AUDIT_TABLE_NAME must be provided in config or environment variables.")

    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)

    item = {
        'MessageId': message.message_id,
        'Timestamp': datetime.datetime.utcnow().isoformat(),
        'ProcessingStatus': processing_status,
        'Payload': json.dumps(message.payload), # Store payload as a string
        'Attributes': json.dumps(message.attributes) # Store attributes as a string
    }

    if audit_data:
        item['AuditData'] = json.dumps(audit_data)

    response = table.put_item(Item=item)

    return {
        "message_id": message.message_id,
        "persisted": True,
        "dynamodb_response_metadata": response['ResponseMetadata']
    }
