import os
import boto3
from typing import Optional, Dict, Any
from botocore.exceptions import ClientError


class SecurityClient:
    """Client helper utilities for AWS Secrets Manager integration."""

    def __init__(self, region: Optional[str] = None):
        """
        Initialize AWS Secrets Manager client.

        Args:
            region: AWS region (defaults to AWS_REGION env var or us-east-1)
        """
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("secretsmanager", region_name=self.region)

    def get_secret(
        self, secret_name: str, version_stage: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get secret value with optional version stage.

        Args:
            secret_name: Name of the secret
            version_stage: Version stage like 'AWSCURRENT' or 'AWSPENDING'

        Returns:
            Dictionary with secret metadata and value
        """
        params = {"SecretId": secret_name}
        if version_stage:
            params["VersionStage"] = version_stage

        try:
            response = self.client.get_secret_value(**params)
            return {
                "name": secret_name,
                "value": response.get("SecretString", ""),
                "arn": response.get("ARN", ""),
                "version_id": response.get("VersionId", ""),
                "version_stages": response.get("VersionStages", []),
                "created_date": response.get("CreatedDate"),
                "region": self.region,
            }
        except ClientError as e:
            raise self._normalize_error(e, secret_name)

    def list_secrets(self, max_results: int = 100) -> list:
        """
        List secrets in the region.

        Args:
            max_results: Maximum number of secrets to return

        Returns:
            List of secret metadata dictionaries
        """
        try:
            response = self.client.list_secrets(MaxResults=max_results)
            return response.get("SecretList", [])
        except ClientError as e:
            raise self._normalize_error(e, "list operation")

    def describe_secret(self, secret_name: str) -> Dict[str, Any]:
        """
        Get detailed metadata about a secret.

        Args:
            secret_name: Name of the secret

        Returns:
            Dictionary with secret description
        """
        try:
            response = self.client.describe_secret(SecretId=secret_name)
            return response
        except ClientError as e:
            raise self._normalize_error(e, secret_name)

    @staticmethod
    def _normalize_error(error: ClientError, context: str) -> Exception:
        """Normalize AWS errors to consistent exception types."""
        error_code = error.response["Error"]["Code"]
        error_msg = error.response["Error"]["Message"]

        if error_code == "ResourceNotFoundException":
            return ValueError(f"Secret {context} not found: {error_msg}")
        elif error_code == "InvalidRequestException":
            return ValueError(f"Invalid request for {context}: {error_msg}")
        elif error_code == "InvalidParameterException":
            return ValueError(f"Invalid parameter for {context}: {error_msg}")
        elif error_code == "AccessDeniedException":
            return PermissionError(f"Access denied for {context}: {error_msg}")
        else:
            return RuntimeError(f"AWS error for {context}: {error_code} - {error_msg}")

    @staticmethod
    def validate_secret_name(name: str) -> bool:
        """
        Validate secret name format.

        Args:
            name: Secret name to validate

        Returns:
            True if name is valid
        """
        # AWS Secrets Manager naming rules
        if not name:
            return False
        if len(name) > 256:
            return False
        # Must contain only alphanumeric characters and /_+=.@-
        import re

        pattern = r"^[a-zA-Z0-9/_+=.@-]+$"
        return bool(re.match(pattern, name))
