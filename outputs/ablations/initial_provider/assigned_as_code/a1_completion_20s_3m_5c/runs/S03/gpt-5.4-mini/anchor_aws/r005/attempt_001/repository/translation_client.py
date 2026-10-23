import os

import boto3


def translation_region(config=None):
    config = config or {}
    return config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")


def translation_client(config=None):
    return boto3.client("translate", region_name=translation_region(config))


def transcribe_client(config=None):
    config = config or {}
    return boto3.client("polly", region_name=config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
