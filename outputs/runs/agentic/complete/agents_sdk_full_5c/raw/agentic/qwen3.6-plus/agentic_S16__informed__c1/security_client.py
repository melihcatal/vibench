"""
Local configuration and client helper utilities for Secret Management.
Provides centralized configuration loading and AWS Secrets Manager client initialization.
"""

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from typing import Optional, Dict, Any

# AWS Secrets Manager provider configuration
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID_ENV = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV = "AWS_SECRET_ACCESS_KEY"


def get_aws_credentials() -> Dict[str, str]:
    """Retrieve AWS credentials from environment variables."""
    access_key = os.environ.get(AWS_ACCESS_KEY_ID_ENV)
    secret_key = os.environ.get(AWS_SECRET_ACCESS_KEY_ENV)

    if not access_key or not secret_key:
        raise ValueError(
            f"AWS credentials not found. Set {AWS_ACCESS_KEY_ID_ENV} and "
            f"{AWS_SECRET_ACCESS_KEY_ENV} environment variables."
        )

    return {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
        "region_name": os.environ.get("AWS_DEFAULT_REGION", DEFAULT_REGION),
    }


def create_secrets_manager_client(region: Optional[str] = None) -> boto3.client:
    """
    Create and configure an AWS Secrets Manager client.

    Args:
        region: Optional AWS region override. Defaults to AWS_DEFAULT_REGION env var.

    Returns:
        Configured boto3 Secrets Manager client instance.
    """
    region_name = region or os.environ.get("AWS_DEFAULT_REGION", DEFAULT_REGION)
    credentials = get_aws_credentials()

    session = boto3.Session(
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=region_name,
    )

    client = session.client("secretsmanager")
    return client


def handle_secrets_error(error: ClientError) -> Dict[str, Any]:
    """
    Handle AWS Secrets Manager client errors and return structured error info.

    Args:
        error: ClientError from boto3 AWS Secrets Manager operations.

    Returns:
        Dictionary with error details including code, message, and metadata.
    """
    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]

    return {
        "success": False,
        "error_code": error_code,
        "error_message": error_message,
        "request_id": error.response.get("ResponseMetadata", {}).get("RequestId", ""),
        "http_status": error.response.get("ResponseMetadata", {}).get("HTTPStatusCode"),
    }


def normalize_secret_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize an AWS Secrets Manager response into a standard format.

    Args:
        response: Raw response dict from AWS Secrets Manager get_secret_value.

    Returns:
        Normalized response with consistent field names and structure.
    """
    normalized = {
        "success": True,
        "arn": response.get("ARN", ""),
        "name": response.get("Name", ""),
        "version_id": response.get("VersionId", ""),
        "version_stage": response.get("VersionStage", []),
        "created_date": response.get("CreatedDate"),
        "secret_metadata": {
            "secret_id": response.get("ARN", ""),
            "created_date": response.get("CreatedDate"),
            "last_changed_date": response.get("LastChangedDate"),
        },
    }

    if "SecretString" in response:
        normalized["secret_string"] = response["SecretString"]
    elif "SecretBinary" in response:
        normalized["secret_binary"] = response["SecretBinary"]

    return normalized
