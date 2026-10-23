import boto3

# Initialize the SQS client
sqs = boto3.client('sqs')

# Define the source and dead-letter queue URLs
source_queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MySourceQueue'
dlq_queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyDeadLetterQueue'


def send_to_dead_letter(message):
    try:
        # Send the message to the dead-letter queue
        response = sqs.send_message(
            QueueUrl=dlq_queue_url,
            MessageBody=message
        )
        print(f'Message sent to dead-letter queue: {response['MessageId']}')
    except Exception as e:
        print(f'Failed to send message to dead-letter queue: {e}')


# Example usage
message = 'This is a failed message.'
send_to_dead_letter(message)