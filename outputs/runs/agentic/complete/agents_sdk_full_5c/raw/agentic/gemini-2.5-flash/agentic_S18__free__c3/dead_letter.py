import boto3
import json
import os
from messaging_client import get_sqs_client

def send_to_dead_letter_queue(dead_letter_queue_url: str, failed_message_body: dict, original_message_id: str = None) -> dict:
    """Sends a failed message to an AWS SQS dead-letter queue.

    Args:
        dead_letter_queue_url: The URL of the SQS dead-letter queue.
        failed_message_body: The dictionary representing the body of the failed message.
        original_message_id: Optional. The message ID of the original message that failed.

    Returns:
        A dictionary containing the response from the SQS send_message operation.
    """
    sqs_client = get_sqs_client()
    
    # Add context about the failure if needed
    message_attributes = {
        'FailedAttempt': {
            'DataType': 'String',
            'StringValue': 'true'
        }
    }
    if original_message_id:
        message_attributes['OriginalMessageId'] = {
            'DataType': 'String',
            'StringValue': original_message_id
        }

    try:
        response = sqs_client.send_message(
            QueueUrl=dead_letter_queue_url,
            MessageBody=json.dumps(failed_message_body),
            MessageAttributes=message_attributes
        )
        return response
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and a configured SQS Dead-Letter Queue)
    # Ensure AWS_REGION environment variable is set.
    # export AWS_REGION="us-east-1"
    # export SQS_DLQ_URL="https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue"

    sqs_dlq_url = os.environ.get("SQS_DLQ_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/ExampleDLQ")
    sample_failed_event = {
        "error_type": "processing_failure",
        "original_payload": {
            "id": "failed-123",
            "data": "some malformed data"
        },
        "failure_reason": "Invalid data format"
    }
    original_msg_id = "original-msg-uuid-123"

    print(f"Sending failed event to DLQ {sqs_dlq_url}:\n{json.dumps(sample_failed_event, indent=2)}")
    try:
        dlq_response = send_to_dead_letter_queue(sqs_dlq_url, sample_failed_event, original_msg_id)
        print(f"Sent to DLQ successfully: {dlq_response}")
    except Exception as e:
        print(f"Failed to send to DLQ: {e}")
