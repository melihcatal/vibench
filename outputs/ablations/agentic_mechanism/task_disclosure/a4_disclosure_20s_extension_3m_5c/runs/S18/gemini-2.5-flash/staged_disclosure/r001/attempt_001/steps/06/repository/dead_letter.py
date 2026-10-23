import boto3
import os

def send_to_dead_letter_queue(queue_url: str, message_body: str):
    """
    Sends a failed message to a specified dead-letter queue in AWS SQS.

    Args:
        queue_url (str): The URL of the dead-letter queue.
        message_body (str): The content of the failed message.
    """
    # AWS SQS client initialization
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in environment variables
    # or configured via AWS CLI.
    sqs = boto3.client(
        'sqs',
        region_name=os.environ.get('AWS_REGION', 'us-east-1') # Example region
    )

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to dead-letter queue: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")

if __name__ == "__main__":
    # Example usage:
    # Replace with your actual dead-letter queue URL
    DEAD_LETTER_QUEUE_URL = os.environ.get('DEAD_LETTER_QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue') 
    FAILED_MESSAGE_CONTENT = "This is a failed message that needs to be processed later."

    send_to_dead_letter_queue(DEAD_LETTER_QUEUE_URL, FAILED_MESSAGE_CONTENT)
