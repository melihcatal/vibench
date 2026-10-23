import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, Optional
import json


class SecurityClient:
    """Client helper utilities for AWS Secrets Manager integration."""

    def __init__(self, region: Optional[str] = None):
        """
        Initialize the security client.

        Args:
            region: AWS region (defaults to AWS_REGION env var or us-east-1)
        """
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        self._client = None

    @property
    def client(self):
        """Lazy-loaded AWS Secrets Manager client."""
        if self._client is None:
            session = boto3.session.Session()
            self._client = session.client(
                service_name="secretsmanager", region_name=self.region
            )
        return self._client

    def get_secret_value(
        self,
        secret_name: str,
        version_id: Optional[str] = None,
        version_stage: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get secret value with optional version parameters.

        Args:
            secret_name: Name of the secret
            version_id: Specific version ID (optional)
            version_stage: Version stage (optional)

        Returns:
            Dictionary with secret metadata and value
        """
        kwargs = {"SecretId": secret_name}
        if version_id:
            kwargs["VersionId"] = version_id
        if version_stage:
            kwargs["VersionStage"] = version_stage

        try:
            response = self.client.get_secret_value(**kwargs)
            return response
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise ValueError(f"Secret {secret_name} not found") from e
            elif error_code == "InvalidRequestException":
                raise ValueError(f"Invalid request for secret {secret_name}") from e
            elif error_code == "InvalidParameterException":
                raise ValueError(f"Invalid parameter for secret {secret_name}") from e
            else:
                raise RuntimeError(f"Error retrieving secret {secret_name}: {e}") from e

    def parse_secret_json(self, secret_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse JSON content from secret response.

        Args:
            secret_response: Response from get_secret_value

        Returns:
            Parsed JSON dictionary
        """
        if "SecretString" not in secret_response:
            raise ValueError("Secret is not in string format")

        try:
            return json.loads(secret_response["SecretString"])
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON in secret") from e

    def validate_db_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate database configuration has required fields.

        Args:
            config: Database configuration dictionary

        Returns:
            True if valid, raises ValueError if invalid
        """
        required_fields = ["host", "port", "username", "password", "database"]
        missing_fields = [field for field in required_fields if field not in config]

        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")

        if not isinstance(config.get("port"), int) or config.get("port") <= 0:
            raise ValueError("Port must be a positive integer")

        return True

    def get_secret_metadata(self, secret_name: str) -> Dict[str, Any]:
        """
        Get metadata about a secret.

        Args:
            secret_name: Name of the secret

        Returns:
            Secret metadata
        """
        try:
            response = self.client.describe_secret(SecretId=secret_name)
            return response
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise ValueError(f"Secret {secret_name} not found") from e
            else:
                raise RuntimeError(f"Error describing secret {secret_name}: {e}") from e
