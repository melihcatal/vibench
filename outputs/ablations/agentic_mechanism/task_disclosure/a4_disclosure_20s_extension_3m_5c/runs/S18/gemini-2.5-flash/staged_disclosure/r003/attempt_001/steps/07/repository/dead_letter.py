import boto3
import os

def send_to_dead_letter_queue(message_body: str, queue_url: str):
    """
    Sends a failed message to an AWS SQS dead-letter queue.

    Args:
        message_body: The content of the failed message.
        queue_url: The URL of the AWS SQS dead-letter queue.
    """
    # AWS credentials will be picked up from environment variables or AWS config file
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set
    sqs = boto3.client('sqs', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to dead-letter queue: {response.get('MessageId')}")
        return response
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")
        raise

if __name__ == "__main__":
    # This is an example of how to use the function.
    # In a real application, the queue_url would likely come from configuration.
    # Replace with your actual SQS dead-letter queue URL
    # Example: export AWS_DEAD_LETTER_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue"
    dead_letter_queue_url = os.environ.get('AWS_DEAD_LETTER_QUEUE_URL')

    if not dead_letter_queue_url:
        print("Please set the AWS_DEAD_LETTER_QUEUE_URL environment variable.")
    else:
        failed_message_content = "This is a message that failed processing and needs to be quarantined."
        send_to_dead_letter_queue(failed_message_content, dead_letter_queue_url)
