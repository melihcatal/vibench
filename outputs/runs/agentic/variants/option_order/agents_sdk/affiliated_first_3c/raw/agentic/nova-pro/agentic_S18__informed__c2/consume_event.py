import os
import boto3

def consume_event(queue_url):
    sqs = boto3.client('sqs', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    return response