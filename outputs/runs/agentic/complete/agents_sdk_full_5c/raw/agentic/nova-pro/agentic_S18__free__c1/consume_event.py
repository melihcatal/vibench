import boto3

sqs = boto3.client('sqs')

def consume_event(queue_url):
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    return response