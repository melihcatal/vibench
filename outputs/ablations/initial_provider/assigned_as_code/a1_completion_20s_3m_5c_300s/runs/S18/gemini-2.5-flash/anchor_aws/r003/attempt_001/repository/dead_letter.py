import os
import json

from messaging_client import MessagingClient
from messaging_models import Message

def dead_letter_event(message: Message, receipt_handle: str, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    queue_url = config.get("queue_url", os.environ.get("SQS_QUEUE_URL")) # Original queue URL
    dead_letter_queue_url = config.get("dead_letter_queue_url", os.environ.get("SQS_DEAD_LETTER_QUEUE_URL"))

    if not dead_letter_queue_url:
        raise ValueError("SQS_DEAD_LETTER_QUEUE_URL must be provided in config or environment variables.")

    messaging_client = MessagingClient(region_name=region_name, dead_letter_queue_url=dead_letter_queue_url)
    sqs_client = messaging_client.get_sqs_client()

    # Optionally delete from original queue if processing failed after consumption but before DLQing
    if queue_url and receipt_handle:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    response = sqs_client.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=message.to_json(),
        MessageAttributes={
            'MessageType': {
                'DataType': 'String',
                'StringValue': 'DeadLetterMessage'
            }
        }
    )
    return {"message_id": response["MessageId"]}
