import boto3
import json
from botocore.exceptions import ClientError
from botocore.config import Config
import os
from messaging_client import SNS_TOPIC_ARN, AWS_REGION
from messaging_models import PubSubEvent

sns_client = boto3.client(
    'sns',
    region_name=AWS_REGION,
    config=Config(retries={'max_attempts': 3})
)

def publish_event(event: PubSubEvent) -> dict:
    """
    Publishes a JSON event to the Amazon SNS topic.
    """
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=json.dumps(event.model_dump()),
            MessageStructure='json'
        )
        return response
    except ClientError as e:
        raise Exception(f"Failed to publish event: {e}")
