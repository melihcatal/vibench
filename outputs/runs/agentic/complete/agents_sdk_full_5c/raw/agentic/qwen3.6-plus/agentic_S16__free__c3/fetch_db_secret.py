"""
Fetch a database connection secret from AWS Secrets Manager.

This module retrieves database credentials (username, password, host, port, etc.)
at runtime from AWS Secrets Manager for secure database connections.
"""

import json
import logging
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from security_client import get_secrets_manager_client
from security_models import SecretFetchResult, DatabaseCredentials

logger = logging.getLogger(__name__)

AWS_PROVIDER_ID = "aws-secrets-manager"
AWS_SECRETS_MANAGER_HOST = "secretsmanager.us-east-1.amazonaws.com"


def fetch_db_secret(secret_name: str, region_name: str = "us-east-1") -> SecretFetchResult:
    """
    Fetch a database connection secret from AWS Secrets Manager.

    Args:
        secret_name: The name or ARN of the database secret.
        region_name: AWS region for Secrets Manager.

    Returns:
        SecretFetchResult containing the database credentials.
    """
    try:
        client = get_secrets_manager_client(region_name=region_name)

        response = client.get_secret_value(SecretId=secret_name)

        secret_string = response.get("SecretString")
        if not secret_string:
            return SecretFetchResult(
                success=False,
                secret_name=secret_name,
                provider=AWS_PROVIDER_ID,
                error="Secret value is missing",
            )

        secret_data = json.loads(secret_string)

        return SecretFetchResult(
            success=True,
            secret_name=secret_name,
            secret_value=secret_string,
            version_id=response.get("VersionId"),
            arn=response.get("ARN"),
            provider=AWS_PROVIDER_ID,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        logger.error("Error fetching DB secret %s from AWS: %s", secret_name, error_code)
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"AWS error: {error_code}",
        )
    except json.JSONDecodeError as e:
        return SecretFetchResult(
            success=False,
            secret_name=secret_name,
            provider=AWS_PROVIDER_ID,
            error=f"Failed to parse secret JSON: {str(e)}",
        )


def extract_db_credentials(secret_name: str, region_name: str = "us-east-1") -> Optional[DatabaseCredentials]:
    """
    Fetch and parse a database secret into a structured DatabaseCredentials object.

    AWS Secrets Manager RDS secrets typically contain:
    - engine, username, password, host, port, dbname

    Args:
        secret_name: The secret name or ARN.
        region_name: AWS region.

    Returns:
        DatabaseCredentials or None if fetch/parsing fails.
    """
    result = fetch_db_secret(secret_name, region_name)
    if not result.success or not result.secret_value:
        return None

    try:
        secret_data = json.loads(result.secret_value)

        return DatabaseCredentials(
            engine=secret_data.get("engine", ""),
            username=secret_data.get("username", ""),
            password=secret_data.get("password", ""),
            host=secret_data.get("host", ""),
            port=secret_data.get("port", 0),
            database=secret_data.get("dbname", ""),
            version_id=result.version_id,
            provider=AWS_PROVIDER_ID,
        )
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error("Failed to extract DB credentials from %s: %s", secret_name, str(e))
        return None
