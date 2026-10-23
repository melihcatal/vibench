# consume_event.py
# [SAME-SCENARIO]
# Consume one message from an Amazon SQS queue (managed subscription)

import json
import os
import boto3
from messaging_client import SqsClient


def consume_event(queue_url):
    """Receive and delete a single message from the SQS queue.

    Args:
        queue_url (str): URL of the SQS queue.

    Returns:
        dict: Parsed JSON message payload or None if empty.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise RuntimeError("AWS credentials not found in environment")

    # Create a boto3 SQS client
    client = boto3.client(
        "sqs",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    sqs = SqsClient(client)

    # Receive up to 1 message (max 10 for batch, but we request 1)
    response = client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=0
    )
    messages = response.get("Messages", [])
    if not messages:
        print("No messages in queue.")
        return None

    raw = messages[0]
    body = raw["Body"]
    receipt_handle = raw["ReceiptHandle"]
    # Parse JSON payload
    payload = json.loads(body)
    print(f"Consumed message ID {raw['MessageId']}")
    # Delete the message after successful handling
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return payload


if __name__ == "__main__":
    # Example usage – set SQS_QUEUE_URL in the environment
    queue = os.getenv("SQS_QUEUE_URL")
    if not queue:
        raise RuntimeError("SQS_QUEUE_URL not set")
    msg = consume_event(queue)
    if msg:
        print("Message payload:", msg)
