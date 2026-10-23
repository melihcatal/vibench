import os
import json
import boto3

class DLQClient:
    def __init__(self):
        self.sqs_client = boto3.client(
            "sqs",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_sqs_client(self):
        return self.sqs_client

def send_to_dead_letter_queue(dlq_url: str, message_body: dict, message_attributes: dict = None):
    client = DLQClient()
    sqs_client = client.get_sqs_client()

    try:
        response = sqs_client.send_message(
            QueueUrl=dlq_url,
            MessageBody=json.dumps(message_body),
            MessageAttributes=message_attributes if message_attributes else {}
        )
        print(f"Message sent to DLQ successfully: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Error sending message to DLQ: {e}")
        raise

if __name__ == '__main__':
    # Example usage:
    # Ensure AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and SQS_DLQ_URL are set as environment variables
    dlq_url = os.environ.get("SQS_DLQ_URL")
    if not dlq_url:
        raise ValueError("SQS_DLQ_URL environment variable not set.")

    failed_message = {
        "original_message_id": "some-uuid-123",
        "error_reason": "Processing failed due to XYZ",
        "original_payload": {
            "user_id": "123",
            "username": "testuser"
        }
    }

    message_attrs = {
        'ErrorType': {
            'DataType': 'String',
            'StringValue': 'ProcessingError'
        }
    }

    send_to_dead_letter_queue(dlq_url, failed_message, message_attrs)
