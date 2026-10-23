import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any


class SecretsManagerClient:
    """Client helper for AWS Secrets Manager operations."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        self._client = None

    @property
    def client(self):
        """Lazy initialization of boto3 client."""
        if self._client is None:
            session = boto3.session.Session()
            self._client = session.client(
                service_name="secretsmanager", region_name=self.region
            )
        return self._client

    def get_secret(
        self, secret_name: str, version_stage: str = "AWSCURRENT"
    ) -> Dict[str, Any]:
        """Get secret value with metadata."""
        try:
            response = self.client.get_secret_value(
                SecretId=secret_name, VersionStage=version_stage
            )

            result = {
                "secret_name": secret_name,
                "value": response.get("SecretString"),
                "version_id": response.get("VersionId"),
                "version_stages": response.get("VersionStages", []),
                "created_date": response.get("CreatedDate"),
                "arn": response.get("ARN"),
            }

            if "SecretBinary" in response:
                result["binary_value"] = response["SecretBinary"]

            return result

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ResourceNotFoundException":
                raise ValueError(f"Secret '{secret_name}' not found")
            elif error_code == "InvalidRequestException":
                raise ValueError(f"Invalid request for secret '{secret_name}'")
            else:
                raise RuntimeError(f"AWS Secrets Manager error: {e}")

    def list_secrets(
        self, max_results: int = 100, filters: Optional[list] = None
    ) -> list:
        """List secrets with optional filtering."""
        try:
            kwargs = {"MaxResults": max_results}
            if filters:
                kwargs["Filters"] = filters

            response = self.client.list_secrets(**kwargs)
            return response.get("SecretList", [])

        except ClientError as e:
            raise RuntimeError(f"Failed to list secrets: {e}")

    def describe_secret(self, secret_name: str) -> Dict[str, Any]:
        """Get detailed information about a secret."""
        try:
            response = self.client.describe_secret(SecretId=secret_name)
            return response
        except ClientError as e:
            raise RuntimeError(f"Failed to describe secret '{secret_name}': {e}")


def load_config() -> Dict[str, Any]:
    """Load configuration from environment variables."""
    config = {
        "aws_region": os.environ.get("AWS_REGION", "us-east-1"),
        "default_secret_stage": os.environ.get("DEFAULT_SECRET_STAGE", "AWSCURRENT"),
        "secret_name_prefix": os.environ.get("SECRET_NAME_PREFIX", ""),
        "enable_rotation": os.environ.get("ENABLE_ROTATION", "false").lower() == "true",
    }
    return config


def normalize_secret_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize secret response to consistent format."""
    normalized = {
        "name": response.get("Name"),
        "value": response.get("SecretString"),
        "version": response.get("VersionId"),
        "stages": response.get("VersionStages", []),
        "created": response.get("CreatedDate"),
        "arn": response.get("ARN"),
    }

    # Add binary data if present
    if "SecretBinary" in response:
        normalized["binary_data"] = response["SecretBinary"]

    # Add rotation info if available
    if "RotationEnabled" in response:
        normalized["rotation_enabled"] = response["RotationEnabled"]

    return normalized
