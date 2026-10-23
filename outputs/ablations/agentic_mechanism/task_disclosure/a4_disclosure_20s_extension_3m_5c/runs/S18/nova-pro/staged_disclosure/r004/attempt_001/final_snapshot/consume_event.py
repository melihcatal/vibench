import boto3

def consume_event():
    sqs = boto3.client('sqs', region_name='us-east-1')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue'
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
    if 'Messages' in response:
        message = response['Messages'][0]
        print('Received message:', message['Body'])
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
    else:
        print('No messages to consume')

if __name__ == '__main__':
    consume_event()