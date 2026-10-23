import os
from functools import lru_cache

import boto3


def _required(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise ValueError(f"missing environment variable: {name}")
    return value


@lru_cache(maxsize=1)
def get_sns_client():
    return boto3.client("sns")


@lru_cache(maxsize=1)
def get_sqs_client():
    return boto3.client("sqs")


def get_topic_arn() -> str:
    return _required("AWS_SNS_TOPIC_ARN")


def get_dead_letter_topic_arn() -> str:
    return os.environ.get("AWS_SNS_DEAD_LETTER_TOPIC_ARN", get_topic_arn())


def get_queue_url() -> str:
    return _required("AWS_SQS_QUEUE_URL")
