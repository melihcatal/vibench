import json
import os

import boto3

from messaging_client import MessagingClient
from messaging_models import PublishRequest

def batch_publish_events(publish_requests: list[PublishRequest], config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION", "us-east-1"))
    topic_arn = config.get("topic_arn", os.environ.get("SNS_TOPIC_ARN"))

    if not topic_arn:
        raise ValueError("SNS_TOPIC_ARN must be provided in config or environment variables.")

    messaging_client = MessagingClient(region_name=region_name, topic_arn=topic_arn)
    sns_client = messaging_client.get_sns_client()

    entries = []
    for i, req in enumerate(publish_requests):
        entry = {
            'Id': str(i),
            'Message': json.dumps(req.event),
        }
        if req.attributes:
            message_attributes = {}
            for key, value in req.attributes.items():
                # AWS SNS MessageAttributes require specific format
                message_attributes[key] = {'DataType': 'String', 'StringValue': str(value)}
            entry['MessageAttributes'] = message_attributes
        entries.append(entry)

    response = sns_client.publish_batch(
        TopicArn=topic_arn,
        PublishBatchRequestEntries=entries
    )

    successful_messages = [{'id': msg['Id'], 'message_id': msg['MessageId']} for msg in response.get('Successful', [])]
    failed_messages = response.get('Failed', [])

    return {
        "successful": successful_messages,
        "failed": failed_messages
    }
