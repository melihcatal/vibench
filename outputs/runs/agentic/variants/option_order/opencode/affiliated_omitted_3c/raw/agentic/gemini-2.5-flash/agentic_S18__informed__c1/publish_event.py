import boto3
import os
import json


def publish_event(topic_arn: str, message: dict, region_name: str = "us-east-1"):
    """
    Publishes a JSON event to an AWS SNS topic.
    """
    sns_client = boto3.client(
        "sns",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )
    response = sns_client.publish(
        TopicArn=topic_arn, Message=json.dumps(message), MessageStructure="json"
    )
    return response
