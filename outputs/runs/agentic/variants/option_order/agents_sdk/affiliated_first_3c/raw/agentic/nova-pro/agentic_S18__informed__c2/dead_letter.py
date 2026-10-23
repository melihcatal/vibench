import os
import boto3

def dead_letter(queue_url, message):
    sqs = boto3.client('sqs', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
    return response