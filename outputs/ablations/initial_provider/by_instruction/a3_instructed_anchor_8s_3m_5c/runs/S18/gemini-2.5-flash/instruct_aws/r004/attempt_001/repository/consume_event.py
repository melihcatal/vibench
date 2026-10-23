import os
import json
import boto3

class ConsumerClient:
    def __init__(self):
        self.sqs_client = boto3.client(
            "sqs",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_sqs_client(self):
        return self.sqs_client

def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 5):
    client = ConsumerClient()
    sqs_client = client.get_sqs_client()

    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            MessageAttributeNames=['All']
        )

        messages = response.get("Messages", [])
        if messages:
            print(f"Received {len(messages)} messages.")
            parsed_messages = []
            for message in messages:
                body = json.loads(message['Body'])
                parsed_messages.append({
                    "receipt_handle": message['ReceiptHandle'],
                    "message_id": message['MessageId'],
                    "body": json.loads(body['Message']),
                    "attributes": body['MessageAttributes']
                })
            return parsed_messages
        else:
            print("No messages received.")
            return []
    except Exception as e:
        print(f"Error consuming event: {e}")
        raise

def delete_message(queue_url: str, receipt_handle: str):
    client = ConsumerClient()
    sqs_client = client.get_sqs_client()
    try:
        sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print(f"Message with receipt handle {receipt_handle} deleted successfully.")
    except Exception as e:
        print(f"Error deleting message: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # Ensure AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and SQS_QUEUE_URL are set as environment variables
    queue_url = os.environ.get("SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("SQS_QUEUE_URL environment variable not set.")

    messages = consume_event(queue_url)
    for msg in messages:
        print(f"Processing message: {msg['body']}")
        # In a real scenario, process the message and then delete it
        # delete_message(queue_url, msg['receipt_handle'])
