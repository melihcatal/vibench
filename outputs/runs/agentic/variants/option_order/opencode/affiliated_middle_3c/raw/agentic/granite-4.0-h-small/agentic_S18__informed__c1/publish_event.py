# publish_event.py
# [SAME-SCENARIO]
# Publish a JSON event to Amazon SNS (managed messaging topic)

import json
import os
import boto3
from messaging_client import SnsClient


def publish_event(topic_arn, payload):
    """Publish a JSON event to the specified SNS topic.

    Args:
        topic_arn (str): ARN of the SNS topic.
        payload (dict): JSON-serializable event payload.
    """
    # Ensure credentials are available via environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise RuntimeError("AWS credentials not found in environment")

    # Create a boto3 SNS client
    client = boto3.client(
        "sns",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    # Wrap with our helper client for consistent interface
    sns = SnsClient(client)
    response = sns.publish(TopicArn=topic_arn, Message=json.dumps(payload))
    print(f"Published event to SNS: {response['MessageId']}")


if __name__ == "__main__":
    # Example usage
    my_topic = os.getenv("SNS_TOPIC_ARN")
    if not my_topic:
        raise RuntimeError("SNS_TOPIC_ARN not set")
    event = {"eventType": "demo", "value": 42, "timestamp": 1734950400}
    publish_event(my_topic, event)
