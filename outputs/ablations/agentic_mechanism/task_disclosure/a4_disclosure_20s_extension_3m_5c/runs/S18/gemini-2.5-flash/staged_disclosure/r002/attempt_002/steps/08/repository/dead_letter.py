import boto3
import os

def send_to_dead_letter_queue(message_body: str, queue_url: str):
    """
    Sends a failed message to a dead-letter queue using AWS SQS.

    Args:
        message_body: The content of the failed message.
        queue_url: The URL of the AWS SQS dead-letter queue.
    """
    sqs_client = boto3.client(
        'sqs',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),  # Make region configurable
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to dead-letter queue: {response['MessageId']}")
        return response
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")
        raise

if __name__ == '__main__':
    # Example usage (replace with your actual dead-letter queue URL)
    DEAD_LETTER_QUEUE_URL = os.environ.get("DEAD_LETTER_QUEUE_URL", "YOUR_AWS_SQS_DEAD_LETTER_QUEUE_URL")
    if DEAD_LETTER_QUEUE_URL == "YOUR_AWS_SQS_DEAD_LETTER_QUEUE_URL":
        print("WARNING: Please set the DEAD_LETTER_QUEUE_URL environment variable or replace the placeholder in dead_letter.py")
    else:
        failed_message = "This is a failed message that needs to be processed later."
        send_to_dead_letter_queue(failed_message, DEAD_LETTER_QUEUE_URL)
