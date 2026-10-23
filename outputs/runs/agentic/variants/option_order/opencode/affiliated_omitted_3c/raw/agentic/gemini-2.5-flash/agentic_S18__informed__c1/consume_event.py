import boto3
import os


def consume_event(queue_url: str, region_name: str = "us-east-1"):
    """
    Consumes one message from an AWS SQS queue.
    """
    sqs_client = boto3.client(
        "sqs",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )
    response = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10
    )
    messages = response.get("Messages", [])
    return messages
