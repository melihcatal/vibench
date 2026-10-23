import os
import json
from messaging_client import get_sqs_client
from messaging_models import OutgoingMessage

def publish_batch_events(messages: list[OutgoingMessage], queue_url: str) -> dict:
    sqs_client = get_sqs_client()
    entries = []
    for i, message in enumerate(messages):
        entry = {
            'Id': message.message_id if message.message_id else str(i),
            'MessageBody': json.dumps(message.dict()),
            'MessageAttributes': {
                'MessageType': {
                    'DataType': 'String',
                    'StringValue': message.message_type
                }
            }
        }
        entries.append(entry)

    try:
        response = sqs_client.send_message_batch(
            QueueUrl=queue_url,
            Entries=entries
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to publish batch messages to SQS: {e}")
