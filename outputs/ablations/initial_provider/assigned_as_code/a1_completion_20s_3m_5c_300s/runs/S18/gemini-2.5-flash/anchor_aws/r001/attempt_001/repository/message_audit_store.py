import json
import os
from typing import Dict, Any

import boto3

from messaging_models import Message

def persist_message_record(message: Message, region_name: str, table_name: str, processing_status: str) -> Dict[str, Any]:
    """
    Persists processed message records to AWS DynamoDB for later lookup.
    The message ID is used as the primary key.
    """
    dynamodb = boto3.resource("dynamodb", region_name=region_name)
    table = dynamodb.Table(table_name)

    record = {
        'message_id': message.id,
        'timestamp': boto3.util.current_time_millis(),
        'body': json.dumps(message.body), # Store body as string
        'attributes': json.dumps(message.attributes), # Store attributes as string
        'processing_status': processing_status
    }

    try:
        table.put_item(Item=record)
        return {"status": "record_persisted", "message_id": message.id, "table_name": table_name}
    except Exception as e:
        return {"status": "error", "message_id": message.id, "details": str(e)}
