import os
from functools import lru_cache
from typing import Dict

import boto3


def require_config() -> Dict[str, str]:
    topic_arn = os.environ["AWS_SNS_TOPIC_ARN"]
    queue_url = os.environ["AWS_SQS_QUEUE_URL"]
    dead_letter_queue_url = os.environ.get("AWS_SQS_DEAD_LETTER_QUEUE_URL", queue_url)
    return {"topic_arn": topic_arn, "queue_url": queue_url, "dead_letter_queue_url": dead_letter_queue_url}


@lru_cache(maxsize=1)
def get_sns_client():
    return boto3.client("sns")


@lru_cache(maxsize=1)
def get_sqs_client():
    return boto3.client("sqs")
