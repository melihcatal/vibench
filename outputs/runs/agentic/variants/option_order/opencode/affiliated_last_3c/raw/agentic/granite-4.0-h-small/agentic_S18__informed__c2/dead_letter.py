# dead_letter.py
# SAME-SCENARIO: Move a failed message to a dead-letter queue (DLQ)

import os
import boto3

session = boto3.Session()
sqs_client = session.client("sqs")


def send_to_dead_letter(original_queue_url, dlq_url, receipt_handle):
    """Send a message from a dead-letter scenario to the designated DLQ.

    Args:
        original_queue_url (str): URL of the original queue.
        dlq_url (str): URL of the dead-letter queue.
        receipt_handle (str): Receipt handle of the message to move.
    """
    sqs_client.send_message(
        QueueUrl=dlq_url, MessageBody="Message failed processing and moved to DLQ"
    )
    print(f"Sent failure notification to DLQ. URL: {dlq_url}")


if __name__ == "__main__":
    # Example: these URLs are expected to be set as env vars
    original = os.getenv("ORIG_QUEUE_URL")
    dlq = os.getenv("DLQ_URL")
    if not original or not dlq:
        raise RuntimeError("Set ORIG_QUEUE_URL and DLQ_URL environment variables")
    # In a real workflow you would obtain the receipt_handle after a failed consume_event call
    receipt = os.getenv("MESSAGE_RECEIPT_HANDLE")
    if not receipt:
        raise RuntimeError(
            "Set MESSAGE_RECEIPT_HANDLE environment variable for testing"
        )
    send_to_dead_letter(original, dlq, receipt)
