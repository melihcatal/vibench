import boto3

def consume_event():
    sqs = boto3.client('sqs', region_name='us-east-1')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue'
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
    if 'Messages' in response:
        message = response['Messages'][0]
        print(f"Received message: {message['Body']}")
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    else:
        print('No messages to consume')

if __name__ == '__main__':
    consume_event()