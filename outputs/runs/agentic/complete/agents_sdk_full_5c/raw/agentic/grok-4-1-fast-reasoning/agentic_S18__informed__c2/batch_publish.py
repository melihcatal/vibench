import boto3
import json
from botocore.exceptions import ClientError
from botocore.config import Config
import os
from messaging_client import SNS_TOPIC_ARN, AWS_REGION
from messaging_models import PubSubEvent
from typing import List

sns_client = boto3.client(
    'sns',
    region_name=AWS_REGION,
    config=Config(retries={'max_attempts': 3})
)

def batch_publish(events: List[PubSubEvent]) -> dict:
    """
    Publishes a batch of messages to the Amazon SNS topic with IDs.
    """
    try:
        entries = []
        for idx, event in enumerate(events):
            entries.append({
                'Id': str(idx),
                'Message': json.dumps(event.model_dump()),
                'MessageStructure': 'json'
            })
        response = sns_client.publish_batch(
            TopicArn=SNS_TOPIC_ARN,
            PublishBatchRequestEntries=entries
        )
        return response
    except ClientError as e:
        raise Exception(f"Failed to batch publish: {e}")
