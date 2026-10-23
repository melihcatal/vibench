from __future__ import annotations

import os
from typing import Dict, Optional

import boto3
from botocore.config import Config
from openai import OpenAI


AWS_KMS_PROVIDER = "aws-kms"
OPENAI_PROVIDER = "openai"
PERSPECTIVE_PROVIDER = "perspective-api"


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    return (
        explicit_region
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION")
        or "us-east-1"
    )


def get_kms_client(region_name: Optional[str] = None):
    return boto3.client(
        "kms",
        region_name=get_aws_region(region_name),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def get_cloudtrail_client(region_name: Optional[str] = None):
    return boto3.client(
        "cloudtrail",
        region_name=get_aws_region(region_name),
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_perspective_config() -> Dict[str, str]:
    return {
        "endpoint": "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        "api_key": os.environ["PERSPECTIVE_API_KEY"],
    }


def normalize_encryption_context(
    encryption_context: Optional[Dict[str, str]],
) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (encryption_context or {}).items()}
