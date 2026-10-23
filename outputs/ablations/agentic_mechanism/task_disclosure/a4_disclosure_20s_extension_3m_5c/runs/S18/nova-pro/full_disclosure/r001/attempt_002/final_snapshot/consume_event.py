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
        receipt_handle = message['ReceiptHandle']
        print(f"Received message: {message['Body']}")
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print("Message deleted.")
    else:
        print("No messages to consume.")

if __name__ == '__main__':
    queue_url = 'YOUR_QUEUE_URL'
    consume_event(queue_url)