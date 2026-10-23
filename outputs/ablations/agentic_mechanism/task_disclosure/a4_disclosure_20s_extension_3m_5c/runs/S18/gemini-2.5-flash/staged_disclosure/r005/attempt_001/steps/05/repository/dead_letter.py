import boto3
import os

def send_to_dead_letter_queue(message_body, queue_url):
    """
    Sends a failed message to an AWS SQS dead-letter queue.

    Args:
        message_body (str): The content of the failed message.
        queue_url (str): The URL of the dead-letter queue.
    """
    try:
        sqs = boto3.client('sqs', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print(f"Message sent to dead-letter queue: {response['MessageId']}")
        return response['MessageId']
    except Exception as e:
        print(f"Error sending message to dead-letter queue: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Ensure AWS_REGION and AWS_DEAD_LETTER_QUEUE_URL environment variables are set
    # For local testing, you might set them like:
    # export AWS_REGION="us-east-1"
    # export AWS_DEAD_LETTER_QUEUE_URL="https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue"
    
    dead_letter_queue_url = os.environ.get('AWS_DEAD_LETTER_QUEUE_URL')
    if dead_letter_queue_url:
        failed_message = "This is a failed message that needs to be processed later."
        send_to_dead_letter_queue(failed_message, dead_letter_queue_url)
    else:
        print("AWS_DEAD_LETTER_QUEUE_URL environment variable not set. Cannot send example message.")
