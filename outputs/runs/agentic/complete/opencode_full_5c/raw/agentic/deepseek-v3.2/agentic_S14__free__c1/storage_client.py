import boto3
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class S3ClientConfig:
    """Configuration for AWS S3 client."""

    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_default_bucket = os.getenv("AWS_DEFAULT_BUCKET")

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.aws_access_key_id:
            raise ValueError("AWS_ACCESS_KEY_ID environment variable is required")
        if not self.aws_secret_access_key:
            raise ValueError("AWS_SECRET_ACCESS_KEY environment variable is required")
        return True


# Global client instance
_s3_client = None
_config = None


def get_s3_config() -> S3ClientConfig:
    """Get or create S3 configuration."""
    global _config
    if _config is None:
        _config = S3ClientConfig()
        _config.validate()
    return _config


def get_s3_client():
    """Get or create AWS S3 client with configuration."""
    global _s3_client
    if _s3_client is None:
        config = get_s3_config()
        _s3_client = boto3.client(
            "s3",
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.aws_region,
        )
    return _s3_client


def get_default_bucket() -> Optional[str]:
    """Get the default bucket from configuration."""
    config = get_s3_config()
    return config.aws_default_bucket


def create_presigned_url_expanded(
    bucket: str,
    key: str,
    operation: str = "get_object",
    expires_in: int = 3600,
    response_headers: dict = None,
) -> str:
    """Create presigned URL with additional options."""
    s3_client = get_s3_client()
    params = {"Bucket": bucket, "Key": key}

    if response_headers:
        params.update(response_headers)

    return s3_client.generate_presigned_url(
        operation, Params=params, ExpiresIn=expires_in
    )
