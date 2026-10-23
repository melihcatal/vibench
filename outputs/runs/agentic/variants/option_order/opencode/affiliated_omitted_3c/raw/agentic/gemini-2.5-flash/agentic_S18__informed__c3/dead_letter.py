import json
import os
from messaging_client import AWSMessagingClient
from messaging_models import MessageConsumptionResult


def send_to_dead_letter_queue(
    message: MessageConsumptionResult, dead_letter_queue_url: str
) -> dict:
    """Sends a failed message to an AWS SQS dead-letter queue."""
    sqs_client = AWSMessagingClient().get_sqs_client()
    try:
        response = sqs_client.send_message(
            QueueUrl=dead_letter_queue_url,
            MessageBody=json.dumps(message.body),
            MessageAttributes={
                key: {"DataType": "String", "StringValue": value}
                for key, value in message.attributes.items()
            },
        )
        return {
            "status": "success",
            "message_id": response["MessageId"],
            "detail": "Message sent to DLQ",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Example Usage (replace with actual DLQ URL and a sample failed message)
    dlq_queue_url = os.environ.get(
        "AWS_DLQ_QUEUE_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/MyDLQ"
    )

    sample_failed_message = MessageConsumptionResult(
        message_id="failed-msg-123",
        receipt_handle="sample-receipt-handle",  # This won't be used for sending to DLQ directly, but part of the consumed message model
        body={
            "original_message": "This message failed processing",
            "error": "Processing timeout",
        },
        attributes={"original_id": "original-msg-id-xyz", "error_reason": "timeout"},
    )

    print(f"Attempting to send message to DLQ: {dlq_queue_url}...")
    result = send_to_dead_letter_queue(sample_failed_message, dlq_queue_url)
    print(result)
