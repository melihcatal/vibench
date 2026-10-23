import os
import json
from messaging_client import get_sqs_client
from messaging_models import IncomingMessage

def send_to_dead_letter_queue(message: IncomingMessage, dlq_url: str, error_reason: str) -> dict:
    sqs_client = get_sqs_client()
    try:
        dlq_message_body = {
            "original_message_id": message.message_id,
            "error_reason": error_reason,
            "original_payload": message.payload,
            "original_attributes": message.attributes,
            "original_message_type": message.message_type
        }
        response = sqs_client.send_message(
            QueueUrl=dlq_url,
            MessageBody=json.dumps(dlq_message_body),
            MessageAttributes={
                'ErrorMessageType': {
                    'DataType': 'String',
                    'StringValue': 'DeadLetter'
                },
                'OriginalMessageType': {
                    'DataType': 'String',
                    'StringValue': message.message_type
                }
            }
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to send message to Dead-Letter Queue: {e}")
