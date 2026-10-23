import json
import os
from typing import Optional, List
from messaging_client import AWSMessagingClient
from messaging_models import MessageConsumptionResult


def consume_event(
    queue_url: str, max_messages: int = 1, wait_time_seconds: int = 5
) -> List[MessageConsumptionResult]:
    """Consumes messages from an AWS SQS queue."""
    sqs_client = AWSMessagingClient().get_sqs_client()
    messages = []
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            MessageAttributeNames=["All"],
        )
        for message in response.get("Messages", []):
            body = json.loads(message["Body"])
            attributes = {
                key: value["StringValue"]
                for key, value in message.get("MessageAttributes", {}).items()
            }
            messages.append(
                MessageConsumptionResult(
                    message_id=message["MessageId"],
                    receipt_handle=message["ReceiptHandle"],
                    body=body,
                    attributes=attributes,
                )
            )
    except Exception as e:
        print(f"Error consuming messages: {e}")
    return messages


def delete_message(queue_url: str, receipt_handle: str) -> dict:
    """Deletes a message from an AWS SQS queue."""
    sqs_client = AWSMessagingClient().get_sqs_client()
    try:
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        return {
            "status": "success",
            "message": f"Message with receipt handle {receipt_handle} deleted.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # Example Usage (replace with actual queue URL)
    sqs_queue_url = os.environ.get(
        "AWS_SQS_QUEUE_URL",
        "https://sqs.us-east-1.amazonaws.com/123456789012/MyTestQueue",
    )

    print(f"Attempting to consume messages from {sqs_queue_url}...")
    consumed_messages = consume_event(sqs_queue_url)
    if consumed_messages:
        for msg in consumed_messages:
            print(f"Consumed message ID: {msg.message_id}, Body: {msg.body}")
            # After processing, delete the message
            # delete_result = delete_message(sqs_queue_url, msg.receipt_handle)
            # print(delete_result)
    else:
        print("No messages available.")
