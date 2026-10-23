import boto3
import json

def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 5):
    sqs_client = boto3.client('sqs')  # AWS SDK import
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time_seconds
    )
    messages = response.get('Messages', [])
    return messages

def delete_message(queue_url: str, receipt_handle: str):
    sqs_client = boto3.client('sqs')
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
