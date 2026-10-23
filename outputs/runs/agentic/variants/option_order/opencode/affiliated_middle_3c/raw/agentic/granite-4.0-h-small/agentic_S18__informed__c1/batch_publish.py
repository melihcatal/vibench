# batch_publish.py
# [SAME-SCENARIO]
# Publish a batch of messages to an Amazon SNS topic

import json
import os
import boto3
from messaging_client import SnsClient


def batch_publish(topic_arn, messages):
    """Publish multiple messages as separate SNS notifications.

    Args:
        topic_arn (str): ARN of the SNS topic.
        messages (list[dict]): List of JSON-serializable message payloads.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise RuntimeError("AWS credentials not found in environment")

    # Single client for the whole batch
    client = boto3.client(
        "sns",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    sns = SnsClient(client)

    for msg in messages:
        response = sns.publish(TopicArn=topic_arn, Message=json.dumps(msg))
        print(f"Batch sent message ID: {response['MessageId']}")


if __name__ == "__main__":
    # Simple CLI: provide topic ARN and a path to a JSON file containing a list of messages
    import sys

    if len(sys.argv) != 3:
        print("Usage: python batch_publish.py <topic_arn> <messages_json_file>")
        sys.exit(1)
    topic = sys.argv[1]
    with open(sys.argv[2]) as f:
        msgs = json.load(f)
    batch_publish(topic, msgs)
