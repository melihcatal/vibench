"""Local configuration and client helper utilities for Managed Model Platform Workflow.

Provides shared AWS Bedrock client initialization, credential resolution,
and retry configuration for the managed model platform workflow.
"""

import os
from typing import Optional

import boto3
from botocore.config import Config


BEDROCK_MODEL_IDS = [
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "anthropic.claude-3-sonnet-20240229-v1:0",
    "anthropic.claude-3-haiku-20240307-v1:0",
    "meta.llama3-70b-instruct-v1:0",
    "mistral.mistral-large-2402-v1:0",
    "amazon.titan-text-express-v1",
]

EMBEDDING_MODEL_IDS = [
    "amazon.titan-embed-text-v2:0",
    "amazon.titan-embed-text-v1",
    "cohere.embed-english-v3",
]


def resolve_bedrock_credentials() -> dict:
    """Resolve AWS credentials from environment or default chain.

    Returns a dict of credential kwargs for boto3 client initialization.
    """
    credentials = {}
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if aws_access_key and aws_secret_key:
        credentials["aws_access_key_id"] = aws_access_key
        credentials["aws_secret_access_key"] = aws_secret_key
    if aws_session_token:
        credentials["aws_session_token"] = aws_session_token

    credentials["region_name"] = aws_region
    return credentials


def create_bedrock_runtime_client(
    credentials: Optional[dict] = None,
    max_retries: int = 5,
) -> boto3.client:
    """Create a configured Amazon Bedrock Runtime client.

    Args:
        credentials: Optional credential dict from resolve_bedrock_credentials.
        max_retries: Number of retry attempts for transient errors.

    Returns:
        Configured boto3 bedrock-runtime client.
    """
    if credentials is None:
        credentials = resolve_bedrock_credentials()

    region = credentials.get("region_name", "us-east-1")
    retry_config = Config(
        retries={"max_attempts": max_retries, "mode": "adaptive"},
        read_timeout=300,
        connect_timeout=30,
    )

    client_kwargs = {
        "service_name": "bedrock-runtime",
        "region_name": region,
        "config": retry_config,
    }
    client_kwargs.update({k: v for k, v in credentials.items() if k != "region_name"})

    return boto3.client(**client_kwargs)


def create_bedrock_client(
    credentials: Optional[dict] = None,
) -> boto3.client:
    """Create a configured Amazon Bedrock control-plane client for model listing.

    Args:
        credentials: Optional credential dict from resolve_bedrock_credentials.

    Returns:
        Configured boto3 bedrock client.
    """
    if credentials is None:
        credentials = resolve_bedrock_credentials()

    region = credentials.get("region_name", "us-east-1")
    client_kwargs = {
        "service_name": "bedrock",
        "region_name": region,
    }
    client_kwargs.update({k: v for k, v in credentials.items() if k != "region_name"})

    return boto3.client(**client_kwargs)


def create_comprehend_client(credentials: Optional[dict] = None) -> boto3.client:
    """Create an Amazon Comprehend client for content safety analysis."""
    if credentials is None:
        credentials = resolve_bedrock_credentials()

    region = credentials.get("region_name", "us-east-1")
    client_kwargs = {
        "service_name": "comprehend",
        "region_name": region,
    }
    client_kwargs.update({k: v for k, v in credentials.items() if k != "region_name"})

    return boto3.client(**client_kwargs)


def create_translate_client(credentials: Optional[dict] = None) -> boto3.client:
    """Create an Amazon Translate client for text translation."""
    if credentials is None:
        credentials = resolve_bedrock_credentials()

    region = credentials.get("region_name", "us-east-1")
    client_kwargs = {
        "service_name": "translate",
        "region_name": region,
    }
    client_kwargs.update({k: v for k, v in credentials.items() if k != "region_name"})

    return boto3.client(**client_kwargs)


def create_polly_client(credentials: Optional[dict] = None) -> boto3.client:
    """Create an Amazon Polly client for text-to-speech synthesis."""
    if credentials is None:
        credentials = resolve_bedrock_credentials()

    region = credentials.get("region_name", "us-east-1")
    client_kwargs = {
        "service_name": "polly",
        "region_name": region,
    }
    client_kwargs.update({k: v for k, v in credentials.items() if k != "region_name"})

    return boto3.client(**client_kwargs)
