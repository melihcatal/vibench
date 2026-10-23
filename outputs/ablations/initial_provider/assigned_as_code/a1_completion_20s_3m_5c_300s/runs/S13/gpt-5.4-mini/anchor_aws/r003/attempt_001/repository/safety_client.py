import os

import boto3


def get_region(config=None):
    config = config or {}
    return config.get("region") or os.environ.get("AWS_REGION") or "us-east-1"


def get_comprehend_client(config=None):
    return boto3.client("comprehend", region_name=get_region(config))


def get_bedrock_runtime_client(config=None):
    config = config or {}
    return boto3.client("bedrock-runtime", region_name=get_region(config))


def get_translate_client(config=None):
    config = config or {}
    return boto3.client("translate", region_name=get_region(config))


def get_polly_client(config=None):
    config = config or {}
    return boto3.client("polly", region_name=get_region(config))
