import os
import boto3
from botocore.exceptions import ClientError


class KeyManagementClient:
    """Thin wrapper around AWS KMS client for simplicity."""

    def __init__(self, service: str = "aws_kms") -> None:
        self.service = service.upper()
        # Environment variables expected by boto3
        # (self‑managed credentials are out of scope for this demo)
        self.client = boto3.client('kms')

    def get_client(self) -> boto3.client:
        """Return the underlying boto3 KMS client."""
        return self.client

    def set_credentials(self, access_key: str, secret_key: str, region: str = "us-east-1") -> None:
        """Override credentials and region – useful for testing against a sandbox."""
        self.client = boto3.client(
            'kms',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

# Helper for other services could be added here with a similar interface.
# The class name and method names follow the same‑scenario file naming convention.
