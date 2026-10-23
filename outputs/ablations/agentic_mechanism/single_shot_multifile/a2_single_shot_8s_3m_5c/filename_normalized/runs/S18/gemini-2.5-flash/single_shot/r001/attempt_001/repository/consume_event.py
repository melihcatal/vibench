import json
import os
from typing import Optional, Dict
from messaging_client import get_sqs_client

def consume_event(queue_url: str, max_number_of_messages: int = 1, wait_time_seconds: int = 20) -> Optional[Dict]:
    sqs_client = get_sqs_client()
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=wait_time_seconds,
        MessageAttributeNames=['All']
    )

    messages = response.get('Messages', [])
    if not messages:
        return None

    message = messages[0]
    body = message.get('Body')
    try:
        parsed_body = json.loads(body)
    except json.JSONDecodeError:
        parsed_body = {"raw_message_body": body}

    return {
        "body": parsed_body,
        "receipt_handle": message.get('ReceiptHandle'),
        "message_id": message.get('MessageId')
    }

def delete_consumed_message(queue_url: str, receipt_handle: str):
    sqs_client = get_sqs_client()
    sqs_client.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )