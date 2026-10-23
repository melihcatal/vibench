"""Local configuration and client helper utilities for Secret Management using AWS Secrets Manager."""

import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import normalize_secret_response


DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
SECRETS_MANAGER_ENDPOINT = os.getenv("SECRETS_MANAGER_ENDPOINT", None)


class SecretsManagerClient:
    """Helper client for interacting with AWS Secrets Manager."""

    def __init__(
        self,
        region_name: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        profile_name: Optional[str] = None,
    ):
        self.region_name = region_name or DEFAULT_REGION
        self.endpoint_url = endpoint_url or SECRETS_MANAGER_ENDPOINT
        self.profile_name = profile_name

        session_kwargs = {}
        if self.profile_name:
            session_kwargs["profile_name"] = self.profile_name

        session = boto3.Session(**session_kwargs)
        config = Config(
            region_name=self.region_name,
            retries={"max_attempts": 3, "mode": "standard"},
        )
        client_kwargs = {"config": config}
        if self.endpoint_url:
            client_kwargs["endpoint_url"] = self.endpoint_url

        self.client = session.client("secretsmanager", **client_kwargs)

    def get_secret_value(
        self,
        secret_id: str,
        version_id: Optional[str] = None,
        version_stage: Optional[str] = "AWSCURRENT",
    ) -> Dict[str, Any]:
        """Retrieve a secret value from AWS Secrets Manager."""
        request_kwargs: Dict[str, Any] = {"SecretId": secret_id}
        if version_id:
            request_kwargs["VersionId"] = version_id
        if version_stage:
            request_kwargs["VersionStage"] = version_stage

        try:
            response = self.client.get_secret_value(**request_kwargs)
            return normalize_secret_response(response)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise KeyError(f"Secret not found: {secret_id}") from e
            elif error_code == "InvalidRequestException":
                raise ValueError(f"Invalid request for secret {secret_id}: {e}") from e
            raise

    def describe_secret(self, secret_id: str) -> Dict[str, Any]:
        """Describe a secret's metadata from AWS Secrets Manager."""
        try:
            return self.client.describe_secret(SecretId=secret_id)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise KeyError(f"Secret not found: {secret_id}") from e
            raise

    def list_secret_version_ids(
        self,
        secret_id: str,
        include_deprecated: bool = False,
        max_results: int = 10,
    ) -> Dict[str, Any]:
        """List version IDs for a secret from AWS Secrets Manager."""
        request_kwargs: Dict[str, Any] = {
            "SecretId": secret_id,
            "MaxResults": max_results,
        }
        if include_deprecated:
            request_kwargs["IncludeDeprecated"] = True

        try:
            return self.client.list_secret_version_ids(**request_kwargs)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise KeyError(f"Secret not found: {secret_id}") from e
            raise


def get_secrets_client() -> SecretsManagerClient:
    """Factory function to get a configured SecretsManagerClient."""
    return SecretsManagerClient()
