import boto3

def consume_event(queue_url):
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        print(f"Received message: {message['Body']}")
        # Delete the message from the queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        print("Message deleted.")
    else:
        print("No messages to consume.")

# Example usage
# consume_event('https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue')