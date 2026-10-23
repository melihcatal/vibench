import os
import json
import boto3


def publish_event(topic_arn: str, message: dict):
    sns_client = boto3.client(
        "sns",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        MessageAttributes={
            "event_type": {
                "DataType": "String",
                "StringValue": message.get("event_type", "unknown"),
            }
        },
    )
    return response
