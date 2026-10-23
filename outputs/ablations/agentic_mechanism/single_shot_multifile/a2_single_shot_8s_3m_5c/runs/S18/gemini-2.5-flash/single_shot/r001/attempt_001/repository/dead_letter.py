import json
import os
from typing import Dict, Optional
from messaging_client import get_sqs_client

def send_to_dead_letter_queue(message_payload: Dict, dlq_queue_url: str, message_attributes: Optional[Dict] = None):
    sqs_client = get_sqs_client()
    message_body = json.dumps(message_payload)

    sqs_message_attributes = {}
    if message_attributes:
        for key, value in message_attributes.items():
            sqs_message_attributes[key] = {
                'DataType': 'String',
                'StringValue': str(value)
            }

    response = sqs_client.send_message(
        QueueUrl=dlq_queue_url,
        MessageBody=message_body,
        MessageAttributes=sqs_message_attributes
    )
    return response