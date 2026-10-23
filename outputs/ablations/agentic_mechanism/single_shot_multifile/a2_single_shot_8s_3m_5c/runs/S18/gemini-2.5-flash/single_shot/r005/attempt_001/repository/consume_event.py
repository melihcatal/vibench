import os
import json
from messaging_client import get_sqs_client
from messaging_models import IncomingMessage

def consume_event(queue_url: str, max_messages: int = 1, wait_time_seconds: int = 10) -> list[IncomingMessage]:
    sqs_client = get_sqs_client()
    messages = []
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            MessageAttributeNames=['All']
        )
        for message_data in response.get('Messages', []):
            body = json.loads(message_data['Body'])
            message_type = message_data['MessageAttributes'].get('MessageType', {}).get('StringValue', 'unknown')
            messages.append(IncomingMessage(
                message_id=message_data['MessageId'],
                receipt_handle=message_data['ReceiptHandle'],
                message_type=message_type,
                payload=body['payload'],
                attributes=body.get('attributes', {})
            ))
        return messages
    except Exception as e:
        raise RuntimeError(f"Failed to consume messages from SQS: {e}")

def delete_consumed_event(queue_url: str, receipt_handle: str) -> dict:
    sqs_client = get_sqs_client()
    try:
        response = sqs_client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Failed to delete message from SQS: {e}")
