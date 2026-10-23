import boto3
import json
from botocore.exceptions import ClientError
from botocore.config import Config
import os
from messaging_client import SQS_DLQ_URL, AWS_REGION
from messaging_models import PubSubMessage

sqs_client = boto3.client(
    'sqs',
    region_name=AWS_REGION,
    config=Config(retries={'max_attempts': 3})
)

def send_to_dead_letter(message: PubSubMessage) -> dict:
    """
    Sends a failed message to the Amazon SQS dead-letter queue.
    """
    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_DLQ_URL,
            MessageBody=message.body,
            MessageAttributes={
                attr_name: {'StringValue': attr_value, 'DataType': 'String'}
                for attr_name, attr_value in message.attributes.items()
            }
        )
        return response
    except ClientError as e:
        raise Exception(f"Failed to send to DLQ: {e}")
