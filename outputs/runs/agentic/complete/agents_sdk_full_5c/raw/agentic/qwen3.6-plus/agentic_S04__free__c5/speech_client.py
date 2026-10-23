"""
Local configuration and client helper utilities for AWS Batch Speech-to-Text.

Provider: AWS Transcribe (amazon.transcribe)
SDK: boto3
"""

import os
from typing import Optional

import boto3
from botocore.config import Config


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_BUCKET = os.getenv("AWS_DEFAULT_BUCKET", "transcription-inputs")


def get_transcribe_client(
    region: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> boto3.client:
    """Return a configured AWS Transcribe client using boto3."""
    region = region or AWS_REGION
    config = Config(
        region_name=region,
        retries={"max_attempts": 5, "mode": "standard"},
    )
    return boto3.client(
        "transcribe",
        aws_access_key_id=aws_access_key_id or AWS_ACCESS_KEY_ID,
        aws_secret_access_key=aws_secret_access_key or AWS_SECRET_ACCESS_KEY,
        config=config,
    )


def get_translate_client(
    region: Optional[str] = None,
) -> boto3.client:
    """Return a configured AWS Translate client."""
    region = region or AWS_REGION
    return boto3.client(
        "translate",
        region_name=region,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def get_comprehend_client(
    region: Optional[str] = None,
) -> boto3.client:
    """Return a configured AWS Comprehend client for content moderation."""
    region = region or AWS_REGION
    return boto3.client(
        "comprehend",
        region_name=region,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def get_bedrock_runtime_client(
    region: Optional[str] = None,
) -> boto3.client:
    """Return a configured AWS Bedrock Runtime client for LLM operations."""
    region = region or AWS_REGION
    return boto3.client(
        "bedrock-runtime",
        region_name=region,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def build_s3_uri(bucket: str, key: str) -> str:
    """Build an S3 URI from bucket and key."""
    return f"s3://{bucket}/{key.lstrip('/')}"


def parse_s3_uri(uri: str) -> tuple[str, str]:
    """Parse an S3 URI into (bucket, key)."""
    if uri.startswith("s3://"):
        uri = uri[5:]
    parts = uri.split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    return bucket, key
