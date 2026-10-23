# messaging_client.py
# HELPER: Central utilities for AWS SNS/SQS interactions

import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import json

# Create a boto3 session using credentials from environment
session = boto3.Session()

sns_client = session.client("sns")
sqs_client = session.client("sqs")


def get_sns_topic_arn(topic_name: str) -> str:
    """Lookup SNS topic ARN by topic name using list_topics.

    Args:
        topic_name (str): The name of the SNS topic.
    Returns:
        str: ARN of the matching topic.
    Raises:
        ValueError: If the topic cannot be found.
    """
    resp = sns_client.list_topics()
    topics = resp.get("Topics", [])
    for t in topics:
        if t["TopicArn"].split(":")[-1] == topic_name:
            return t["TopicArn"]
    raise ValueError(f"SNS topic '{topic_name}' not found.")


def get_sqs_queue_url(queue_name: str) -> str:
    """Lookup SQS queue URL by queue name.

    Args:
        queue_name (str): The name of the SQS queue.
    Returns:
        str: URL of the matching queue.
    Raises:
        ValueError: If queue not found.
    """
    resp = sqs_client.list_queues(QueueNamePrefix=queue_name)
    urls = resp.get("QueueUrls", [])
    for url in urls:
        if url.split("/")[-1] == queue_name:
            return url
    raise ValueError(f"SQS queue '{queue_name}' not found.")


def publish_event(topic_arn: str, payload: dict) -> None:
    """Publish a JSON payload to SNS.

    Args:
        topic_arn (str): ARN of the SNS topic.
        payload (dict): JSON-serializable payload.
    """
    try:
        sns_client.publish(TopicArn=topic_arn, Message=json.dumps(payload))
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"SNS publish error: {e}")


def consume_event(queue_url: str, wait_seconds: int = 20) -> dict:
    """Receive and delete a single message from SQS.

    Args:
        queue_url (str): URL of the SQS queue.
        wait_seconds (int): Long poll wait time.
    Returns:
        dict: Parsed JSON body of the message.
    Raises:
        RuntimeError: If no message or processing fails.
    """
    resp = sqs_client.receive_message(
        QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=wait_seconds
    )
    msgs = resp.get("Messages", [])
    if not msgs:
        raise RuntimeError("No message in queue.")
    message = msgs[0]
    receipt_handle = message["ReceiptHandle"]
    payload = json.loads(message["Body"])
    # Delete after successful processing
    sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    return payload


if __name__ == "__main__":
    # Simple demo that publishes then consumes a test message
    topic_name = os.getenv("DEMO_TOPIC_NAME", "demo-topic")
    queue_name = os.getenv("DEMO_QUEUE_NAME", "demo-queue")
    topic_arn = get_sns_topic_arn(topic_name)
    queue_url = get_sqs_queue_url(queue_name)
    payload = {"demoId": 1, "msg": "Hello helper"}
    publish_event(topic_arn, payload)
    received = consume_event(queue_url)
    print("Consumed demo payload:", received)
