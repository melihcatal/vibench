import boto3
import json
import os
from messaging_client import get_sqs_client

def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 5) -> list:
    """Consumes messages from an AWS SQS queue.

    Args:
        queue_url: The URL of the SQS queue.
        max_messages: The maximum number of messages to retrieve (1 to 10).
        wait_time_seconds: The duration (in seconds) for which the call waits
                           for a message to arrive in the queue before returning.

    Returns:
        A list of dictionaries, where each dictionary represents a consumed message.
        Includes 'Body' (parsed JSON), 'MessageId', 'ReceiptHandle'.
    """
    sqs_client = get_sqs_client()
    messages = []
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            MessageAttributeNames=['All']
        )
        
        if 'Messages' in response:
            for msg in response['Messages']:
                try:
                    message_body = json.loads(msg['Body'])
                    messages.append({
                        "Body": message_body,
                        "MessageId": msg['MessageId'],
                        "ReceiptHandle": msg['ReceiptHandle']
                    })
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode message body as JSON: {msg['Body']}")
                    messages.append({
                        "Body": msg['Body'], # Keep raw body if not JSON
                        "MessageId": msg['MessageId'],
                        "ReceiptHandle": msg['ReceiptHandle']
                    })
        return messages
    except Exception as e:
        print(f"Error consuming message from SQS: {e}")
        raise

def delete_message(queue_url: str, receipt_handle: str) -> dict:
    """Deletes a message from an AWS SQS queue.

    Args:
        queue_url: The URL of the SQS queue.
        receipt_handle: The receipt handle of the message to delete.

    Returns:
        A dictionary containing the response from the SQS delete operation.
    """
    sqs_client = get_sqs_client()
    try:
        response = sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return response
    except Exception as e:
        print(f"Error deleting message from SQS: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and a configured SQS queue)
    # Ensure AWS_REGION environment variable is set.
    # export AWS_REGION="us-east-1"
    # export SQS_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/123456789012/MyEventQueue"
    
    sqs_queue_url = os.environ.get("SQS_QUEUE_URL", "https://sqs.us-east-1.amazonaws.com/123456789012/ExampleQueue")
    print(f"Consuming messages from {sqs_queue_url}...")
    try:
        received_messages = consume_event(sqs_queue_url, max_messages=1)
        if received_messages:
            for msg in received_messages:
                print(f"Received MessageId: {msg['MessageId']}")
                print(f"Body: {json.dumps(msg['Body'], indent=2)}")
                # After processing, delete the message
                # delete_response = delete_message(sqs_queue_url, msg['ReceiptHandle'])
                # print(f"Message deleted: {delete_response}")
        else:
            print("No messages received.")
    except Exception as e:
        print(f"Failed to consume: {e}")
