import boto3
import os

sns = boto3.client('sns', region_name='us-east-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def publish_event(topic_arn, message):
    response = sns.publish(TopicArn=topic_arn, Message=message)
    return response