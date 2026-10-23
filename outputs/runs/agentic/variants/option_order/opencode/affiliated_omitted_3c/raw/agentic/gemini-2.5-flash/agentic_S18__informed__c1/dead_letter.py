import boto3
import os
import json


def send_to_dead_letter_queue(
    queue_url: str, message_body: dict, region_name: str = "us-east-1"
):
    """
    Sends a failed message to an AWS SQS dead-letter queue.
    """
    sqs_client = boto3.client(
        "sqs",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name,
    )
    response = sqs_client.send_message(
        QueueUrl=queue_url, MessageBody=json.dumps(message_body)
    )
    return response
