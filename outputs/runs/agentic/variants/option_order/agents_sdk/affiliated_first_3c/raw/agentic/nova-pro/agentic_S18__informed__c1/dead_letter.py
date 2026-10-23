import boto3
import os
sqs = boto3.client('sqs', region_name='us-east-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def dead_letter(queue_url, message):
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message)
    return response