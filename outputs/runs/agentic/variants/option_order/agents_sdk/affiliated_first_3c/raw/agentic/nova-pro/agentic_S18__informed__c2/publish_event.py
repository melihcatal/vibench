import os
import boto3

def publish_event(topic_arn, message):
    sns = boto3.client('sns', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = sns.publish(TopicArn=topic_arn, Message=message)
    return response