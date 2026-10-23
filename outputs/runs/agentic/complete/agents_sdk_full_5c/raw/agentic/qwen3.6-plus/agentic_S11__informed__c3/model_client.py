"""Local configuration and client helper utilities for Managed Model Platform Workflow.

Provider: Amazon Bedrock via boto3
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import os
from typing import Optional

import boto3
from botocore.config import Config


BEDROCK_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
BEDROCK_RUNTIME_SERVICE = "bedrock-runtime"
BEDROCK_SERVICE = "bedrock"


def get_aws_region() -> str:
    """Return the configured AWS region."""
    return os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_bedrock_runtime_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Bedrock Runtime client (boto3) for inference calls.

    Uses AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY from environment
    or explicit parameters. Targets the bedrock-runtime endpoint for
    model invocation, streaming, and embedding operations.
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=300,
    )
    return boto3.client(
        service_name=BEDROCK_RUNTIME_SERVICE,
        region_name=region_name or get_aws_region(),
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY"),
        config=config,
    )


def get_bedrock_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Bedrock control-plane client (boto3) for model listing.

    Uses the bedrock (non-runtime) endpoint to query foundation model
    metadata and list available model IDs.
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
    )
    return boto3.client(
        service_name=BEDROCK_SERVICE,
        region_name=region_name or get_aws_region(),
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY"),
        config=config,
    )


def get_translate_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Translate client."""
    return boto3.client(
        service_name="translate",
        region_name=region_name or get_aws_region(),
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_polly_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Polly client for text-to-speech synthesis."""
    return boto3.client(
        service_name="polly",
        region_name=region_name or get_aws_region(),
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_comprehend_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> boto3.client:
    """Create an Amazon Comprehend client for content safety analysis."""
    return boto3.client(
        service_name="comprehend",
        region_name=region_name or get_aws_region(),
        aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )
