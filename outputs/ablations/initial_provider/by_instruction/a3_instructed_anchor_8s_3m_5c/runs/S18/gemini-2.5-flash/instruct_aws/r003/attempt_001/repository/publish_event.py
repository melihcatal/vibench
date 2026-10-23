import boto3
import json
from messaging_client import get_sns_client

def publish_event(topic_arn: str, message: dict):
    sns_client = get_sns_client()
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        MessageStructure='json'
    )
    return response
