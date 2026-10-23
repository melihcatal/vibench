import os

import boto3


def get_bedrock_runtime_client(config=None):
    config = config or {}
    region = config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("bedrock-runtime", region_name=region)


def get_bedrock_client(config=None):
    config = config or {}
    region = config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("bedrock", region_name=region)
