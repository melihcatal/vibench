"""Provide local configuration and client helper utilities for Secret Management.

This module wraps AWS Secrets Manager (boto3) client creation with
configuration loading, retry settings, and credential handling.
"""

import os
import logging
from functools import lru_cache
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)

# AWS Secrets Manager provider configuration
AWS_SM_ENDPOINT_URL = os.environ.get("AWS_SM_ENDPOINT_URL", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_MAX_ATTEMPTS = int(os.environ.get("AWS_MAX_ATTEMPTS", "3"))
AWS_RETRY_MODE = os.environ.get("AWS_RETRY_MODE", "standard")


def get_aws_credentials() -> dict:
    """Load AWS credentials from environment or fall back to default chain."""
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN", ""),
    }


def get_secrets_client(region: str = None) -> boto3.client:
    """Create a configured AWS Secrets Manager client using boto3.

    Args:
        region: AWS region; defaults to AWS_DEFAULT_REGION env var or us-east-1.

    Returns:
        Configured boto3 client for AWS Secrets Manager (secretsmanager service).
    """
    target_region = region or AWS_DEFAULT_REGION
    credentials = get_aws_credentials()
    # Filter out empty credential values so boto3 uses its default chain
    filtered_creds = {k: v for k, v in credentials.items() if v}

    retry_config = Config(
        retries={
            "max_attempts": AWS_MAX_ATTEMPTS,
            "mode": AWS_RETRY_MODE,
        }
    )

    session = boto3.Session(
        region_name=target_region,
        **filtered_creds,
    )

    client_kwargs = {
        "service_name": "secretsmanager",
        "config": retry_config,
    }
    if AWS_SM_ENDPOINT_URL:
        client_kwargs["endpoint_url"] = AWS_SM_ENDPOINT_URL

    client = session.client(**client_kwargs)
    logger.info("AWS Secrets Manager client created for region %s", target_region)
    return client


@lru_cache(maxsize=4)
def get_cached_secrets_client(region: str = None) -> boto3.client:
    """Return a cached AWS Secrets Manager client for the given region."""
    return get_secrets_client(region=region)


def validate_secrets_access(region: str = None) -> bool:
    """Validate that we can access AWS Secrets Manager by listing secrets.

    Returns True if the client can successfully list secrets, False otherwise.
    """
    try:
        client = get_secrets_client(region=region)
        client.list_secrets(MaxResults=1)
        return True
    except ClientError as exc:
        logger.warning("AWS Secrets Manager access validation failed: %s", exc)
        return False
