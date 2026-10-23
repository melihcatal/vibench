import os
import json
from typing import Dict, Any
from messaging_client import MessagingClient
from messaging_models import PubsubMessage

def send_to_dead_letter_queue(dead_letter_queue_url: str, original_message: PubsubMessage, error_details: str) -> Dict[str, Any]:
    """Sends a failed message to an AWS SQS dead-letter queue.

    Args:
        dead_letter_queue_url: The URL of the dead-letter SQS queue.
        original_message: The original PubsubMessage that failed processing.
        error_details: A string detailing the reason for the failure.

    Returns:
        A dictionary containing the response from AWS SQS.
    """
    client = MessagingClient()
    sqs_client = client.sns_client.meta.client # Re-using the boto3 session for SQS

    # Prepare the message to be sent to the dead-letter queue
    # It's good practice to include the original message and error details
    dead_letter_payload = {
        "original_message_id": original_message.message_id,
        "original_data": original_message.data,
        "original_attributes": original_message.attributes,
        "error_details": error_details,
        "timestamp": "", # Add a timestamp here in a real scenario
    }

    response = sqs_client.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=json.dumps(dead_letter_payload),
        MessageAttributes={
            "failureReason": {"DataType": "String", "StringValue": error_details},
            "originalMessageId": {"DataType": "String", "StringValue": original_message.message_id},
        }
    )
    return response

if __name__ == '__main__':
    dead_letter_queue_url = os.environ.get("DEAD_LETTER_QUEUE_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/my-dead-letter-queue")
    
    # Simulate a failed message
    failed_message = PubsubMessage(
        message_id="failed-msg-123",
        data={"action": "process_payment", "transaction_id": "abc", "amount": 100},
        attributes={"event_type": "payment", "status": "failed"}
    )
    error_info = "Payment processing failed due to insufficient funds."

    print(f"Sending failed message to dead-letter queue: {dead_letter_queue_url}")
    try:
        dlq_response = send_to_dead_letter_queue(dead_letter_queue_url, failed_message, error_info)
        print("Message sent to DLQ successfully:", dlq_response)
    except Exception as e:
        print(f"Error sending to dead-letter queue: {e}")
