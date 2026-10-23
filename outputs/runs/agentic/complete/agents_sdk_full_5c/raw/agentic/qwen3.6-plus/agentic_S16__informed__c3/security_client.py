"""
Local configuration and client helper utilities for Secret Management.
Provides AWS Secrets Manager client initialization, credential loading,
and common retry/backoff helpers for secret retrieval operations.
"""

import os
import time
import logging
from typing import Optional, Dict, Any

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")

MAX_RETRIES = 3
BACKOFF_BASE = 0.5

_SECRETS_MANAGER_CLIENT = None


def get_aws_config() -> Config:
    """Build a botocore Config with retry and timeout settings."""
    return Config(
        region_name=AWS_REGION,
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=5,
        read_timeout=10,
    )


def get_secrets_manager_client() -> boto3.client:
    """
    Return a cached boto3 client for AWS Secrets Manager.

    Provider: AWS Secrets Manager
    SDK: boto3
    Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    """
    global _SECRETS_MANAGER_CLIENT
    if _SECRETS_MANAGER_CLIENT is not None:
        return _SEcrets_MANAGER_CLIENT

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    _SECRETS_MANAGER_CLIENT = session.client("secretsmanager", config=get_aws_config())
    return _SECRETS_MANAGER_CLIENT


def reset_client() -> None:
    """Reset the cached client (useful for testing)."""
    global _SECRETS_MANAGER_CLIENT
    _SECRETS_MANAGER_CLIENT = None


def retry_with_backoff(func, *args, **kwargs):
    """Execute *func* with exponential backoff on retriable ClientError."""
    attempt = 0
    while attempt < MAX_RETRIES:
        try:
            return func(*args, **kwargs)
        except ClientError as exc:
            code = exc.response["Error"].get("Code", "")
            if code in (
                "ThrottlingException",
                "ProvisionedThroughputExceededException",
            ):
                attempt += 1
                if attempt >= MAX_RETRIES:
                    raise
                delay = BACKOFF_BASE * (2 ** (attempt - 1))
                logger.warning(
                    "Retriable error (%s), attempt %d/%d, sleeping %.1fs",
                    code,
                    attempt,
                    MAX_RETRIES,
                    delay,
                )
                time.sleep(delay)
            else:
                raise
    return None


def validate_secret_name(name: str) -> bool:
    """Basic validation for an AWS Secrets Manager secret name."""
    if not name or len(name) < 1 or len(name) > 512:
        return False
    if "/" in name or "\\" in name:
        return False
    return True
