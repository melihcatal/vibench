import boto3
import os
import json

def send_to_dead_letter_queue(message_body: dict, queue_url: str):
    """
    Sends a failed message to an AWS SQS dead-letter queue.

    Args:
        message_body (dict): The content of the failed message.
        queue_url (str): The URL of the SQS dead-letter queue.
    """
    try:
        sqs = boto3.client(
            'sqs',
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1") # Default region
        )
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body)
        )
        print(f"Message sent to dead-letter queue: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")

if __name__ == "__main__":
    # Example usage:
    # Ensure you have AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEAD_LETTER_QUEUE_URL
    # environment variables set up.
    # Replace with your actual dead-letter queue URL
    dead_letter_queue_url = os.environ.get("AWS_DEAD_LETTER_QUEUE_URL")

    if dead_letter_queue_url:
        failed_message = {
            "error": "Processing failed due to XYZ",
            "original_payload": {"id": "123", "data": "some_data"}
        }
        send_to_dead_letter_queue(failed_message, dead_letter_queue_url)
    else:
        print("Please set the AWS_DEAD_LETTER_QUEUE_URL environment variable.")
