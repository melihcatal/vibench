import boto3
import json

from messaging_client import get_sns_client
from messaging_models import normalize_payload


def consume_event(queue_url: str):
    sqs = boto3.client('sqs', region_name='us-west-2')
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        payload = json.loads(message['Body'])
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        return payload
    return None