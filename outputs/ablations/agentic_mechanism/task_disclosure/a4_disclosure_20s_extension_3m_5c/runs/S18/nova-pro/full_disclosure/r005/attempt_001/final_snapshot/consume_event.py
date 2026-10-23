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
        print(f"Consumed message: {message['Body']}")
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
    else:
        print("No messages to consume")

if __name__ == '__main__':
    queue_url = 'YOUR_QUEUE_URL'
    consume_event(queue_url)