import boto3
import os

def send_to_dead_letter_queue(message_body, queue_url=None):
    """
    Sends a failed message to an AWS SQS dead-letter queue.

    Args:
        message_body (str): The content of the failed message.
        queue_url (str, optional): The URL of the dead-letter queue.
                                   If not provided, it tries to read from DEAD_LETTER_QUEUE_URL env var.
    """
    if queue_url is None:
        queue_url = os.environ.get("DEAD_LETTER_QUEUE_URL")

    if not queue_url:
        print("Error: Dead-letter queue URL not provided and DEAD_LETTER_QUEUE_URL environment variable is not set.")
        return

    try:
        sqs = boto3.client("sqs")
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to dead-letter queue: {response['MessageId']}")
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set the environment variable before running, or pass the queue_url directly
    # os.environ["DEAD_LETTER_QUEUE_URL"] = "YOUR_DEAD_LETTER_QUEUE_URL"
    failed_message = "This is a message that failed processing."
    send_to_dead_letter_queue(failed_message, "https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue") # Replace with your actual SQS Dead Letter Queue URL
