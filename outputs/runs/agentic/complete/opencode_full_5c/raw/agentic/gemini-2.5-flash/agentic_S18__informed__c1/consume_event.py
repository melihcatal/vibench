import os
import boto3


def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 20):
    sqs_client = boto3.client(
        "sqs",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time_seconds,
    )
    messages = response.get("Messages", [])
    return messages


def delete_message(queue_url: str, receipt_handle: str):
    sqs_client = boto3.client(
        "sqs",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
    response = sqs_client.delete_message(
        QueueUrl=queue_url, ReceiptHandle=receipt_handle
    )
    return response
