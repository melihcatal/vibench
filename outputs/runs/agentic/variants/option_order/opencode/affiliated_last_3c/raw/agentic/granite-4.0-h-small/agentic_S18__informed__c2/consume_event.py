# consume_event.py
# SAME-SCENARIO: Pull a single message from Amazon SQS queue representing SNS subscription

import os
import json
import boto3

session = boto3.Session()
sqs_client = session.client("sqs")


def consume_event(queue_url, wait_seconds=20):
    """Receive a single message from the SQS queue.

    Args:
        queue_url (str): URL of the SQS queue.
        wait_seconds (int, optional): Long poll wait time. Defaults to 20.

    Returns:
        dict or None: Decoded JSON payload or None if queue empty.
    """
    response = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=wait_seconds
    )
    if "Messages" not in response or len(response["Messages"]) == 0:
        print("No messages in queue.")
        return None
    message = response["Messages"][0]
    receipt_handle = message["ReceiptHandle"]
    # Assume payload is JSON string
    payload = json.loads(message["Body"])
    print(f"Consumed message: {payload}")
    # Delete message after processing
    sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return payload


if __name__ == "__main__":
    # Example usage: expect SQS queue URL in environment variable
    queue_url = os.getenv("CONSUME_QUEUE_URL")
    if not queue_url:
        raise RuntimeError("Set CONSUME_QUEUE_URL environment variable")
    consume_event(queue_url)
