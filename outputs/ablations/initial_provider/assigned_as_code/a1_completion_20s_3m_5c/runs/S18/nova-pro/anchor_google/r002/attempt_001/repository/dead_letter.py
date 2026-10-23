import boto3
import json

from messaging_client import get_sns_client
from messaging_models import normalize_payload


def dead_letter(message: Dict[str, Any], topic_arn: str):
    sns = get_sns_client()
    sns.publish(
        TopicArn=topic_arn,
        Message=normalize_payload(message)
    )