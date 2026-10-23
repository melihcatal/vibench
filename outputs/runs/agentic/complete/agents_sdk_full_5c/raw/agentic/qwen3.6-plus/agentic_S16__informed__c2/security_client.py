"""Local configuration and client helper utilities for Secret Management.

Provides AWS Secrets Manager client creation and secret-name resolution
utilities used across the secret-management integration files.

Provider: AWS Secrets Manager (boto3)
"""

import os
from typing import Any

import boto3
from botocore.config import Config


def get_secret_manager_client(region: str | None = None) -> Any:
    """Create and return a boto3 Secrets Manager client.

    Reads AWS credentials from environment:
      - AWS_ACCESS_KEY_ID
      - AWS_SECRET_ACCESS_KEY
      - AWS_DEFAULT_REGION (optional fallback)
    """
    resolved_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
    )

    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=resolved_region,
    )

    return session.client("secretsmanager", config=config)


def resolve_secret_name(
    explicit_name: str | None,
    default_env: str = "SECRET_NAME",
) -> str:
    """Resolve the secret name from an explicit value or an environment variable.

    Raises ValueError if neither is provided.
    """
    name = explicit_name or os.environ.get(default_env)
    if not name:
        raise ValueError(
            f"No secret name provided. Pass secret_name or set {default_env}."
        )
    return name


def normalize_secret_payload(raw_value: str) -> dict:
    """Normalize a raw secret payload into a consistent dict structure."""
    import json

    try:
        parsed = json.loads(raw_value)
        if isinstance(parsed, dict):
            return parsed
        return {"value": parsed}
    except json.JSONDecodeError:
        return {"raw_value": raw_value}
