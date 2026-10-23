# messaging_client.py
# [HELPER]
# Local configuration and reusable client wrappers for Pub/Sub messaging (Amazon SNS/SQS)

import os
import boto3


class SnsClient:
    """Thin wrapper around boto3 SNS client with helpful methods."""

    def __init__(self, client):
        self._client = client

    def publish(self, TopicArn, Message):
        """Publish a single message to the SNS topic."""
        return self._client.publish(TopicArn=TopicArn, Message=Message)

    def publish_batch(self, TopicArn, messages):
        """Optional helper for batch publishing (calls publish for each)."""
        for m in messages:
            self.publish(TopicArn, m)


class SqsClient:
    """Thin wrapper around boto3 SQS client with helpful methods."""

    def __init__(self, client):
        self._client = client

    def receive_message(self, QueueUrl, MaxNumberOfMessages=1, WaitTimeSeconds=0):
        return self._client.receive_message(
            QueueUrl=QueueUrl,
            MaxNumberOfMessages=MaxNumberOfMessages,
            WaitTimeSeconds=WaitTimeSeconds,
        )

    def delete_message(self, QueueUrl, ReceiptHandle):
        self._client.delete_message(QueueUrl=QueueUrl, ReceiptHandle=ReceiptHandle)

    def send_message(self, QueueUrl, MessageBody, DelaySeconds=0):
        self._client.send_message(
            QueueUrl=QueueUrl, MessageBody=MessageBody, DelaySeconds=DelaySeconds
        )


def get_sns_client(region="us-east-1"):
    """Return a configured SnsClient using environment credentials."""
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_key or not aws_secret:
        raise RuntimeError("AWS credentials not set in environment")
    client = boto3.client(
        "sns",
        region_name=region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
    )
    return SnsClient(client)


def get_sqs_client(region="us-east-1"):
    """Return a configured SqsClient using environment credentials."""
    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret = os.getenv("AWS_SECRET_ACCESS_KEY")
    if not aws_key or not aws_secret:
        raise RuntimeError("AWS credentials not set in environment")
    client = boto3.client(
        "sqs",
        region_name=region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
    )
    return SqsClient(client)


def get_queue_url(queue_name):
    """Resolve a queue name to its URL (requires queue already created)."""
    client = boto3.client("sqs")
    response = client.list_queues(QueueNamePrefix=queue_name)
    if not response.get("QueueUrls"):
        raise ValueError(f"Queue {queue_name} not found")
    return response["QueueUrls"][0]


if __name__ == "__main__":
    # Quick test harness (unset for production use)
    import json

    sns = get_sns_client()
    sqs = get_sqs_client()
    topic = os.getenv("SNS_TOPIC_ARN")
    queue_name = os.getenv("SQS_QUEUE_NAME")
    if topic and queue_name:
        url = get_queue_url(queue_name)
        print("SNS:", topic, "| SQS URL:", url)
