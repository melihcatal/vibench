import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any
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
        """Lazy-loaded boto3 Secrets Manager client."""
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
        Get secret value with error handling.

        Args:
            secret_name: Name of the secret
            version_id: Specific version ID (optional)
            version_stage: Version stage (optional)

        Returns:
            Dictionary containing secret response
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
            error_msg = e.response["Error"]["Message"]

            if error_code == "ResourceNotFoundException":
                raise ValueError(
                    f"Secret '{secret_name}' not found: {error_msg}"
                ) from e
            elif error_code == "InvalidRequestException":
                raise ValueError(
                    f"Invalid request for secret '{secret_name}': {error_msg}"
                ) from e
            elif error_code == "InvalidParameterException":
                raise ValueError(
                    f"Invalid parameter for secret '{secret_name}': {error_msg}"
                ) from e
            elif error_code == "InvalidParameterValueException":
                raise ValueError(
                    f"Invalid version specified for secret '{secret_name}': {error_msg}"
                ) from e
            else:
                raise RuntimeError(
                    f"Error retrieving secret '{secret_name}': {error_msg}"
                ) from e

    def parse_secret_string(self, secret_response: Dict[str, Any]) -> str:
        """
        Extract secret string from response.

        Args:
            secret_response: Response from get_secret_value

        Returns:
            Secret string value
        """
        if "SecretString" in secret_response:
            return secret_response["SecretString"]
        else:
            raise ValueError("Secret is not in string format")

    def parse_json_secret(self, secret_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse JSON-formatted secret from response.

        Args:
            secret_response: Response from get_secret_value

        Returns:
            Parsed JSON dictionary
        """
        secret_string = self.parse_secret_string(secret_response)

        try:
            parsed_data = json.loads(secret_string)
            if not isinstance(parsed_data, dict):
                raise ValueError("Secret JSON is not a dictionary")
            return parsed_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in secret: {e}") from e

    def normalize_db_config(self, secret_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize database connection configuration.

        Args:
            secret_data: Parsed secret data

        Returns:
            Normalized database configuration
        """
        return {
            "host": secret_data.get("host") or secret_data.get("endpoint"),
            "port": secret_data.get("port", 5432),
            "database": secret_data.get("database") or secret_data.get("dbname"),
            "username": secret_data.get("username") or secret_data.get("user"),
            "password": secret_data.get("password"),
            "engine": secret_data.get("engine", "postgres"),
        }

    def list_secret_versions(self, secret_name: str) -> list:
        """
        List all versions of a secret.

        Args:
            secret_name: Name of the secret

        Returns:
            List of secret versions
        """
        try:
            response = self.client.list_secret_version_ids(SecretId=secret_name)
            return response.get("Versions", [])
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_msg = e.response["Error"]["Message"]
            raise RuntimeError(
                f"Error listing versions for secret '{secret_name}': {error_msg}"
            ) from e
