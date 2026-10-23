"""
Local configuration and client helper utilities for Secret Management.

Provides factory functions for creating AWS Secrets Manager clients
and handles credential loading and region configuration.
"""

import os
from typing import Optional

import boto3
from botocore.config import Config

AWS_SECRETS_MANAGER_HOST = "secretsmanager.us-east-1.amazonaws.com"
DEFAULT_REGION = "us-east-1"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3


def get_aws_access_key() -> Optional[str]:
    """Retrieve AWS access key from environment or IAM role."""
    return os.environ.get("AWS_ACCESS_KEY_ID")


def get_aws_secret_key() -> Optional[str]:
    """Retrieve AWS secret access key from environment or IAM role."""
    return os.environ.get("AWS_SECRET_ACCESS_KEY")


def get_aws_session_token() -> Optional[str]:
    """Retrieve AWS session token from environment."""
    return os.environ.get("AWS_SESSION_TOKEN")


def get_aws_region() -> str:
    """Retrieve configured AWS region."""
    return os.environ.get("AWS_DEFAULT_REGION", DEFAULT_REGION)


def get_secrets_manager_config() -> Config:
    """
    Build a botocore Config object for Secrets Manager client.

    Returns:
        Configured botocore.config.Config instance.
    """
    return Config(
        retries={"max_attempts": DEFAULT_RETRIES, "mode": "standard"},
        connect_timeout=DEFAULT_TIMEOUT,
        read_timeout=DEFAULT_TIMEOUT,
        signature_version="v4",
    )


def get_secrets_manager_client(
    region_name: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> boto3.client:
    """
    Create and return an AWS Secrets Manager boto3 client.

    Uses environment credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN) or IAM role credentials automatically.

    Args:
        region_name: AWS region override.
        endpoint_url: Custom endpoint override for testing or local development.

    Returns:
        Configured boto3 Secrets Manager client.
    """
    region = region_name or get_aws_region()
    config = get_secrets_manager_config()

    client_kwargs = {
        "service_name": "secretsmanager",
        "region_name": region,
        "config": config,
    }

    access_key = get_aws_access_key()
    secret_key = get_aws_secret_key()
    session_token = get_aws_session_token()

    if access_key and secret_key:
        client_kwargs["aws_access_key_id"] = access_key
        client_kwargs["aws_secret_access_key"] = secret_key
        if session_token:
            client_kwargs["aws_session_token"] = session_token

    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url
    else:
        client_kwargs["endpoint_url"] = f"https://secretsmanager.{region}.amazonaws.com"

    session = boto3.Session()
    client = session.client(**client_kwargs)
    return client
