import os
from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def get_settings():
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "topic_arn": os.getenv("AWS_SNS_TOPIC_ARN", ""),
        "queue_url": os.getenv("AWS_SQS_QUEUE_URL", ""),
        "dead_letter_queue_url": os.getenv("AWS_SQS_DLQ_URL", ""),
        "audit_table_name": os.getenv("AWS_DYNAMODB_AUDIT_TABLE", ""),
    }


@lru_cache(maxsize=1)
def sns_client():
    return boto3.client("sns", region_name=get_settings()["aws_region"])


@lru_cache(maxsize=1)
def sqs_client():
    return boto3.client("sqs", region_name=get_settings()["aws_region"])


@lru_cache(maxsize=1)
def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=get_settings()["aws_region"])
