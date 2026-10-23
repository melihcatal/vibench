from __future__ import annotations

import os
from typing import Optional

import boto3
from botocore.config import Config


DEFAULT_AWS_REGION = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
DEFAULT_KMS_SIGNING_ALGORITHM = os.getenv("AWS_KMS_SIGNING_ALGORITHM", "RSASSA_PSS_SHA_256")
DEFAULT_KMS_KEY_SPEC = os.getenv("AWS_KMS_KEY_SPEC", "SYMMETRIC_DEFAULT")



def aws_region() -> str:
    return DEFAULT_AWS_REGION



def kms_client(region_name: Optional[str] = None):
    return boto3.client(
        "kms",
        region_name=region_name or aws_region(),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )



def cloudtrail_client(region_name: Optional[str] = None):
    return boto3.client(
        "cloudtrail",
        region_name=region_name or aws_region(),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )



def bedrock_runtime_client(region_name: Optional[str] = None):
    return boto3.client(
        "bedrock-runtime",
        region_name=region_name or aws_region(),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )
