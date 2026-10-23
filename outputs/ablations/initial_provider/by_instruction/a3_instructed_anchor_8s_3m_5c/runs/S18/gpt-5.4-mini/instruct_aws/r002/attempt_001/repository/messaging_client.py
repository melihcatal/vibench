import os
from typing import Any, Dict, Optional
import boto3


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def sns_client():
    return boto3.client("sns", region_name=aws_region())


def sqs_client():
    return boto3.client("sqs", region_name=aws_region())


def resolve_queue_url(queue_url: Optional[str] = None) -> str:
    return queue_url or os.environ["SQS_QUEUE_URL"]


def resolve_topic_arn(topic_arn: Optional[str] = None) -> str:
    return topic_arn or os.environ["SNS_TOPIC_ARN"]


def message_attributes(attributes: Optional[Dict[str, Dict[str, str]]] = None) -> Dict[str, Dict[str, str]]:
    return attributes or {}
