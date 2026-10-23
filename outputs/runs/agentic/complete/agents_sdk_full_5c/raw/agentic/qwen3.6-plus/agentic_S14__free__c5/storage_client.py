"""
Local configuration and client helper utilities for Managed Object Storage.

Provides connection setup, credential handling, and shared client instances
for AWS S3 managed object storage operations.
"""

import os
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


# AWS S3 provider configuration constants
S3_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_DEFAULT_BUCKET = os.getenv("S3_DEFAULT_BUCKET", "")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", None)
S3_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
S3_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
S3_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN", None)

# Provider-identifying environment variables for AWS
AWS_CONFIG_FILE = os.getenv("AWS_CONFIG_FILE", os.path.expanduser("~/.aws/config"))
AWS_CREDENTIALS_FILE = os.getenv(
    "AWS_SHARED_CREDENTIALS_FILE", os.path.expanduser("~/.aws/credentials")
)
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")


class StorageClientConfig:
    """Configuration container for S3 managed object storage client."""

    def __init__(
        self,
        region: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
        session_token: Optional[str] = None,
        profile: Optional[str] = None,
        default_bucket: Optional[str] = None,
        max_retries: int = 3,
        connect_timeout: int = 5,
        read_timeout: int = 30,
    ):
        self.region = region or S3_DEFAULT_REGION
        self.endpoint_url = endpoint_url or S3_ENDPOINT_URL
        self.access_key_id = access_key_id or S3_ACCESS_KEY_ID
        self.secret_access_key = secret_access_key or S3_SECRET_ACCESS_KEY
        self.session_token = session_token or S3_SESSION_TOKEN
        self.profile = profile or AWS_PROFILE
        self.default_bucket = default_bucket or S3_DEFAULT_BUCKET
        self.max_retries = max_retries
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout


class StorageClient:
    """
    Managed client wrapper for AWS S3 object storage.

    Provides singleton-like behavior with lazy initialization and
    shared configuration across storage operations.
    """

    _instance = None

    def __init__(self, config: Optional[StorageClientConfig] = None):
        self.config = config or StorageClientConfig()
        self._s3_client = None
        self._s3_resource = None

    @classmethod
    def get_instance(cls, config: Optional[StorageClientConfig] = None) -> "StorageClient":
        """Return the shared StorageClient singleton instance."""
        if cls._instance is None:
            cls._instance = cls(config)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        if cls._instance is not None:
            cls._instance._s3_client = None
            cls._instance._s3_resource = None
            cls._instance = None

    def _build_client_config(self) -> Config:
        return Config(
            region_name=self.config.region,
            retries={"max_attempts": self.config.max_retries},
            connect_timeout=self.config.connect_timeout,
            read_timeout=self.config.read_timeout,
            s3={"addressing_style": "path"} if self.config.endpoint_url else {},
        )

    def get_s3_client(self):
        """Get or create the boto3 S3 client."""
        if self._s3_client is None:
            kwargs = {
                "config": self._build_client_config(),
            }
            if self.config.endpoint_url:
                kwargs["endpoint_url"] = self.config.endpoint_url
            if self.config.access_key_id and self.config.secret_access_key:
                kwargs["aws_access_key_id"] = self.config.access_key_id
                kwargs["aws_secret_access_key"] = self.config.secret_access_key
                if self.config.session_token:
                    kwargs["aws_session_token"] = self.config.session_token
            elif self.config.profile:
                kwargs["profile_name"] = self.config.profile

            self._s3_client = boto3.client("s3", **kwargs)
        return self._s3_client

    def get_s3_resource(self):
        """Get or create the boto3 S3 resource."""
        if self._s3_resource is None:
            kwargs = {
                "config": self._build_client_config(),
            }
            if self.config.endpoint_url:
                kwargs["endpoint_url"] = self.config.endpoint_url
            if self.config.access_key_id and self.config.secret_access_key:
                kwargs["aws_access_key_id"] = self.config.access_key_id
                kwargs["aws_secret_access_key"] = self.config.secret_access_key
                if self.config.session_token:
                    kwargs["aws_session_token"] = self.config.session_token
            elif self.config.profile:
                kwargs["profile_name"] = self.config.profile

            self._s3_resource = boto3.resource("s3", **kwargs)
        return self._s3_resource

    def get_bucket(self, bucket_name: Optional[str] = None):
        """Get an S3 bucket resource reference."""
        resource = self.get_s3_resource()
        name = bucket_name or self.config.default_bucket
        if not name:
            raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")
        return resource.Bucket(name)

    def validate_bucket_exists(self, bucket_name: Optional[str] = None) -> bool:
        """Check if the S3 bucket exists and is accessible."""
        client = self.get_s3_client()
        name = bucket_name or self.config.default_bucket
        if not name:
            return False
        try:
            client.head_bucket(Bucket=name)
            return True
        except ClientError:
            return False


def get_client(config: Optional[StorageClientConfig] = None) -> StorageClient:
    """Convenience function to get the shared storage client."""
    return StorageClient.get_instance(config)


def parse_s3_uri(uri: str) -> tuple:
    """Parse an s3:// URI into (bucket, key) tuple."""
    if not uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {uri}")
    path = uri[5:]
    parts = path.split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    return bucket, key


def format_s3_uri(bucket: str, key: str) -> str:
    """Format bucket and key into an s3:// URI."""
    return f"s3://{bucket}/{key}"
