import os

import boto3


def load_messaging_config():
    return {
        "region": os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        "topic_arn": os.getenv("SNS_TOPIC_ARN"),
        "queue_url": os.getenv("SQS_QUEUE_URL"),
        "dead_letter_queue_url": os.getenv("SQS_DEAD_LETTER_QUEUE_URL"),
    }


def sns_client(region=None):
    return boto3.client("sns", region_name=region)


def sqs_client(region=None):
    return boto3.client("sqs", region_name=region)
