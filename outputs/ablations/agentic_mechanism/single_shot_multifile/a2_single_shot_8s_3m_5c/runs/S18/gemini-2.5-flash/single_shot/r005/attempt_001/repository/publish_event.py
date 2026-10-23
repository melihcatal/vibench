import os
import json
from messaging_client import get_sqs_client
from messaging_models import OutgoingMessage

def publish_event(message: OutgoingMessage, queue_url: str) -> dict:
    sqs_client = get_sqs_client()
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message.dict()),
            MessageAttributes={
                'MessageType': {
                    'DataType': 'String',
                    'StringValue': message.message_type
                }
            }
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to publish message to SQS: {e}")
