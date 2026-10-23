"""
Managed Object Storage client helper utilities.

Uses Amazon S3 (boto3) as the concrete provider.
Provider signals:
  - boto3 import
  - S3 service identifier
  - AWS environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional


class S3StorageClient:
    """Wrapper around boto3 S3 client with configuration and common utilities."""

    def __init__(
        self,
        bucket: Optional[str] = None,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
    ):
        self.bucket = bucket or os.environ.get("AWS_BUCKET_NAME", "")
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.endpoint_url = endpoint_url

        session_kwargs = {}
        access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        if access_key and secret_key:
            session_kwargs["aws_access_key_id"] = access_key
            session_kwargs["aws_secret_access_key"] = secret_key

        self.config = Config(
            signature_version="s3v4",
            retries={"max_attempts": 3, "mode": "standard"},
            region_name=self.region,
        )

        self.client = boto3.client(
            "s3",
            config=self.config,
            endpoint_url=self.endpoint_url,
            **session_kwargs,
        )

    def ensure_bucket_exists(self) -> bool:
        """Check if the configured bucket exists."""
        try:
            self.client.head_bucket(Bucket=self.bucket)
            return True
        except ClientError:
            return False

    def build_object_key(self, prefix: str, filename: str) -> str:
        """Build a normalized S3 object key from prefix and filename."""
        prefix = prefix.strip("/")
        if prefix:
            return f"{prefix}/{filename}"
        return filename

    def get_client(self):
        """Return the underlying boto3 S3 client."""
        return self.client
