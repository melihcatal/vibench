from __future__ import annotations

import os
from typing import Optional

import boto3


def get_aws_region() -> str:
    return (
        os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1"
    )


def get_kms_key_id(explicit_key_id: Optional[str] = None) -> str:
    key_id = explicit_key_id or os.getenv("AWS_KMS_KEY_ID")
    if not key_id:
        raise ValueError("AWS_KMS_KEY_ID is required")
    return key_id


def get_kms_client():
    return boto3.client("kms", region_name=get_aws_region())


def get_cloudtrail_client():
    return boto3.client("cloudtrail", region_name=get_aws_region())


def get_bedrock_runtime_client():
    return boto3.client("bedrock-runtime", region_name=get_aws_region())


def get_comprehend_client():
    return boto3.client("comprehend", region_name=get_aws_region())


def get_translate_client():
    return boto3.client("translate", region_name=get_aws_region())
