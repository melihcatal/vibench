# dead_letter.py
# [SAME-SCENARIO]
# Send a failed message to a dead-letter queue (DLQ) using Amazon SQS

import json
import os
import boto3
from messaging_client import SqsClient


def send_to_dlq(failed_message, dlq_url):
    """Send a failed message payload to a dead-letter queue.

    Args:
        failed_message (dict): The original message dict.
        dlq_url (str): URL of the SQS DLQ.
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise RuntimeError("AWS credentials not found in environment")

    client = boto3.client(
        "sqs",
        region_name="us-east-1",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    sqs = SqsClient(client)

    sqs.send_message(
        QueueUrl=dlq_url, MessageBody=json.dumps(failed_message), DelaySeconds=0
    )
    print(f"Sent failed message to DLQ (MessageId: {failed_message.get('id')})")


if __name__ == "__main__":
    # Example CLI usage; DLQ_URL must be provided in the environment
    import sys

    if len(sys.argv) < 3:
        print("Usage: python dead_letter.py <dlq_url> <message_json_file>")
        sys.exit(1)
    dlq_url = sys.argv[1]
    with open(sys.argv[2]) as f:
        failed_message = json.load(f)
    send_to_dlq(failed_message, dlq_url)
