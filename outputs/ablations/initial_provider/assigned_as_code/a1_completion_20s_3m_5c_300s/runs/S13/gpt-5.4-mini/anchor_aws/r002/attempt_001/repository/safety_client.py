import os

import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.environ.get("AWS_REGION") or "us-east-1"


def get_comprehend_client(config=None):
    return boto3.client("comprehend", region_name=get_region(config))
