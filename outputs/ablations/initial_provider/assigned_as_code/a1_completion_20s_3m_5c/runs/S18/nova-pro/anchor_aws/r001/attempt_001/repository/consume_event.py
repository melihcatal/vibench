import boto3

def consume_event():
    sqs = boto3.client('sqs', region_name='us-west-2')
    queue_url = 'https://sqs.us-west-2.amazonaws.com/123456789012/MyQueue'
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
    if 'Messages' in response:
        message = response['Messages'][0]
        print(f'Received message: {message['Body']}')
        return message
    return None