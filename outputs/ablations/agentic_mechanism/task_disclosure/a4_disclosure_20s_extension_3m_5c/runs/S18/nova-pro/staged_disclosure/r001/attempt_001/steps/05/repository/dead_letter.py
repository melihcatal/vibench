import boto3

# Initialize the SQS client
sqs = boto3.client('sqs')

# Specify the URL of the source queue and the dead-letter queue
source_queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/SourceQueue'
dlq_queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/DeadLetterQueue'

def send_to_dead_letter(message_body):
    try:
        # Send the message to the source queue
        response = sqs.send_message(
            QueueUrl=source_queue_url,
            MessageBody=message_body
        )
        print(f'Message sent to source queue: {response['MessageId']}')
    except Exception as e:
        print(f'Failed to send message to source queue: {e}')
        # Send the message to the dead-letter queue
        response = sqs.send_message(
            QueueUrl=dlq_queue_url,
            MessageBody=message_body
        )
        print(f'Message sent to dead-letter queue: {response['MessageId']}')

# Example usage
send_to_dead_letter('This is a test message')