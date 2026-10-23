from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.config import Config


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_boto3_session() -> boto3.session.Session:
    return boto3.session.Session(region_name=get_aws_region())


def get_sqs_client():
    return get_boto3_session().client("sqs", config=Config(retries={"max_attempts": 5, "mode": "standard"}))


def get_sns_client():
    return get_boto3_session().client("sns", config=Config(retries={"max_attempts": 5, "mode": "standard"}))


def get_sqs_queue_url(explicit_queue_url: Optional[str] = None) -> str:
    queue_url = explicit_queue_url or os.getenv("SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("SQS_QUEUE_URL is required")
    return queue_url


def get_dead_letter_queue_url(explicit_queue_url: Optional[str] = None) -> str:
    queue_url = explicit_queue_url or os.getenv("SQS_DEAD_LETTER_QUEUE_URL")
    if not queue_url:
        raise ValueError("SQS_DEAD_LETTER_QUEUE_URL is required")
    return queue_url


def get_sns_topic_arn(explicit_topic_arn: Optional[str] = None) -> str:
    topic_arn = explicit_topic_arn or os.getenv("SNS_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("SNS_TOPIC_ARN is required")
    return topic_arn
