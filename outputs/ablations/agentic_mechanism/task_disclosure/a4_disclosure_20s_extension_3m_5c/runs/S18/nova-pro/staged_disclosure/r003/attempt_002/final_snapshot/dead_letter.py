import boto3

def send_to_dead_letter(message, queue_url, dead_letter_queue_url):
    sqs = boto3.client('sqs')
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
        print(f'Message sent to the queue: {response['MessageId']}')
    except Exception as e:
        print(f'Failed to send message: {e}')
        response = sqs.send_message(
            QueueUrl=dead_letter_queue_url,
            MessageBody=message
        )
        print(f'Message sent to the dead-letter queue: {response['MessageId']}')

# Example usage
send_to_dead_letter('Hello, World!', 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue', 'https://sqs.us-east-1.amazonaws.com/123456789012/DeadLetterQueue')