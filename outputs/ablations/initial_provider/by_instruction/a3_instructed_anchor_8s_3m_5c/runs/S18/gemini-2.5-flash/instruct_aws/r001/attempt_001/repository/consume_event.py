import os
import json
from typing import Dict, Any, Optional, List
from messaging_client import MessagingClient
from messaging_models import PubsubMessage

def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 5) -> List[PubsubMessage]:
    """Consumes messages from an AWS SQS queue.

    Args:
        queue_url: The URL of the AWS SQS queue.
        max_messages: The maximum number of messages to retrieve (1 to 10).
        wait_time_seconds: The duration (in seconds) for which the call waits for a message to arrive in the queue (0 to 20).

    Returns:
        A list of PubsubMessage objects.
    """
    client = MessagingClient()
    sqs_client = client.sns_client.meta.client # Re-using the boto3 session for SQS

    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=['All'],
        VisibilityTimeout=30 # Message is hidden for 30 seconds while processing
    )

    messages: List[PubsubMessage] = []
    for message in response.get("Messages", []):
        message_id = message.get("MessageId", "N/A")
        receipt_handle = message.get("ReceiptHandle")
        body = json.loads(message.get("Body", "{}"))

        attributes = {}
        sqs_message_attributes = message.get("MessageAttributes", {})
        for key, value_dict in sqs_message_attributes.items():
            if "StringValue" in value_dict:
                attributes[key] = value_dict["StringValue"]
            elif "BinaryValue" in value_dict:
                attributes[key] = value_dict["BinaryValue"].decode('utf-8') # Assuming UTF-8 for binary attributes

        # SNS messages published to SQS will have the actual message in the 'Message' field of the 'body'
        sns_message_content = json.loads(body.get("Message", "{}"))
        
        messages.append(PubsubMessage(message_id, sns_message_content, attributes))

        # In a real application, you would process the message here and then delete it.
        # For this example, we'll just print and acknowledge (delete) immediately.
        print(f"Received message: ID={message_id}, Body={sns_message_content}")
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )

    return messages

if __name__ == '__main__':
    queue_url = os.environ.get("SQS_QUEUE_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/my-test-queue")
    print(f"Consuming events from {queue_url}")
    try:
        consumed_messages = consume_event(queue_url)
        if not consumed_messages:
            print("No messages received.")
    except Exception as e:
        print(f"Error consuming events: {e}")
