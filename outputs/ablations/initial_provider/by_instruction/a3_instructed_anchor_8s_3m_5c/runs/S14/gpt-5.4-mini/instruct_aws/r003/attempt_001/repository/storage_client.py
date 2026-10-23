import os
from typing import Optional

import boto3


def get_aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_s3_client(region: Optional[str] = None):
    return boto3.client("s3", region_name=region or get_aws_region())


def get_rekognition_client(region: Optional[str] = None):
    return boto3.client("rekognition", region_name=region or get_aws_region())


def get_translate_client(region: Optional[str] = None):
    return boto3.client("translate", region_name=region or get_aws_region())


def get_bedrock_runtime_client(region: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region or get_aws_region())
