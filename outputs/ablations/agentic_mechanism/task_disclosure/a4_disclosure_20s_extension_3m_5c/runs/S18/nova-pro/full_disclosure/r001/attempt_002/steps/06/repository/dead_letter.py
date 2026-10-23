import boto3

# Initialize a boto3 client for SQS
sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

def send_to_dead_letter(message_body, dead_letter_queue_url):
    try:
        response = sqs.send_message(
            QueueUrl=dead_letter_queue_url,
            MessageBody=message_body
        )
        print(f'Message sent to dead-letter queue. MessageId: {response['MessageId']}')
    except Exception as e:
        print(f'Failed to send message to dead-letter queue: {e}')

# Example usage
# send_to_dead_letter('Failed message body', 'https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue')