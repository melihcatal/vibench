import os
import json
from messaging_client import get_sqs_client
from messaging_models import EventMessage

def send_to_dead_letter(dead_letter_queue_url: str, original_event: EventMessage, error_details: dict) -> dict:
    sqs_client = get_sqs_client()
    dead_letter_payload = {
        "original_event": original_event.to_dict(),
        "error_details": error_details
    }
    response = sqs_client.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=json.dumps(dead_letter_payload),
        MessageAttributes={
            'EventType': {
                'DataType': 'String',
                'StringValue': original_event.event_type
            },
            'Status': {
                'DataType': 'String',
                'StringValue': 'DEAD_LETTER'
            }
        }
    )
    return response
