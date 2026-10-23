import json
import os

from messaging_client import MessagingClient
from messaging_models import Message, ConsumeResponse

def consume_event(config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    queue_url = config.get("queue_url", os.environ.get("SQS_QUEUE_URL"))

    if not queue_url:
        raise ValueError("SQS_QUEUE_URL must be provided in config or environment variables.")

    messaging_client = MessagingClient(region_name=region_name, queue_url=queue_url)
    sqs_client = messaging_client.get_sqs_client()

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )

    messages = response.get("Messages", [])
    if messages:
        sqs_message = messages[0]
        message = Message.from_sqs_message(sqs_message)
        return ConsumeResponse(message, sqs_message['ReceiptHandle'])
    return None
