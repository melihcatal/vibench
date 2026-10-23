import boto3
import json

from messaging_client import get_sns_client
from messaging_models import normalize_payload


def batch_publish(messages: List[Dict[str, Any]], topic_arn: str):
    sns = get_sns_client()
    for message in messages:
        sns.publish(
            TopicArn=topic_arn,
            Message=normalize_payload(message)
        )