import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
import os
from messaging_client import SQS_QUEUE_URL, AWS_REGION
from messaging_models import PubSubMessage
from typing import List

sqs_client = boto3.client(
    'sqs',
    region_name=AWS_REGION,
    config=Config(retries={'max_attempts': 3})
)

def consume_event(max_messages: int = 1, wait_time_seconds: int = 10) -> List[PubSubMessage]:
    """
    Consumes one or more messages from the Amazon SQS queue.
    """
    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            MessageAttributeNames=['All']
        )
        messages = []
        for msg in response.get('Messages', []):
            pubsub_msg = PubSubMessage(
                message_id=msg['MessageId'],
                body=msg['Body'],
                receipt_handle=msg['ReceiptHandle'],
                attributes={k: v['StringValue'] for k, v in msg.get('MessageAttributes', {}).items()}
            )
            messages.append(pubsub_msg)
        return messages
    except ClientError as e:
        raise Exception(f"Failed to consume event: {e}")
