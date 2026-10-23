import os
from functools import lru_cache

import boto3


def _env(name, default=None):
    value = os.getenv(name)
    return value if value not in (None, "") else default


@lru_cache(maxsize=1)
def aws_session():
    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))
    profile = _env("AWS_PROFILE")
    if profile:
        return boto3.Session(profile_name=profile, region_name=region)
    return boto3.Session(region_name=region)


def sns_topic_arn():
    return _env("SNS_TOPIC_ARN")


def sqs_queue_url():
    return _env("SQS_QUEUE_URL")


def dead_letter_queue_url():
    return _env("DEAD_LETTER_QUEUE_URL", sqs_queue_url())


def sns_client():
    return aws_session().client("sns")


def sqs_client():
    return aws_session().client("sqs")


def client_for_destination():
    if sns_topic_arn():
        return sns_client()
    return sqs_client()
