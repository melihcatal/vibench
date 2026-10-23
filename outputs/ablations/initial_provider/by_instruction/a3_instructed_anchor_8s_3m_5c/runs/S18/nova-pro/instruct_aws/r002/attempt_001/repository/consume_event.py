import boto3

def consume_event(queue_url):
    sqs = boto3.client('sqs')
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10,
    )
    return response