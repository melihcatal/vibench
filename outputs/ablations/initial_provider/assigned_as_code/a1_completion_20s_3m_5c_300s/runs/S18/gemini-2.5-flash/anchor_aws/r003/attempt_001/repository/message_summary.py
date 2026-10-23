import os

from messaging_client import MessagingClient
from messaging_models import Message

def summarize_message_processing(message: Message, receipt_handle: str, success: bool, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    queue_url = config.get("queue_url", os.environ.get("SQS_QUEUE_URL"))

    if not queue_url:
        raise ValueError("SQS_QUEUE_URL must be provided in config or environment variables.")

    messaging_client = MessagingClient(region_name=region_name, queue_url=queue_url)
    sqs_client = messaging_client.get_sqs_client()

    if success:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        status = "acknowledged"
    else:
        # For failed messages, allow them to return to the queue for retry
        # or move to a dead-letter queue by not deleting them here.
        # The dead_letter.py function would handle sending to DLQ.
        status = "processed_with_failure"

    return {
        "message_id": message.message_id,
        "status": status,
        "summary": f"Message {message.message_id} processed with {'success' if success else 'failure'}."
    }
