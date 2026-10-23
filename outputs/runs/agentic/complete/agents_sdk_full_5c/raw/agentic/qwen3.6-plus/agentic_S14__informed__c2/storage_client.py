"""
storage_client.py - Provide local configuration and client helper utilities
for Managed Object Storage integration with Amazon S3.
"""
from __future__ import annotations

import os
import io
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


# Environment variable names for Amazon S3 authentication
S3_REGION_ENV = "AWS_DEFAULT_REGION"
S3_ACCESS_KEY_ENV = "AWS_ACCESS_KEY_ID"
S3_SECRET_KEY_ENV = "AWS_SECRET_ACCESS_KEY"
S3_SESSION_TOKEN_ENV = "AWS_SESSION_TOKEN"
S3_ENDPOINT_URL_ENV = "AWS_S3_ENDPOINT"

DEFAULT_REGION = "us-east-1"


def get_s3_config(
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    max_retries: int = 3,
) -> Config:
    """Build an Amazon S3 boto3 configuration object."""
    return Config(
        region_name=region or os.environ.get(S3_REGION_ENV, DEFAULT_REGION),
        retries={"max_attempts": max_retries, "mode": "adaptive"},
        s3={
            "addressing_style": "path",
            "use_accelerate_endpoint": False,
        },
    )


def get_credentials(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
) -> Dict[str, str]:
    """Resolve S3 credentials from parameters or environment variables."""
    return {
        "aws_access_key_id": aws_access_key_id or os.environ.get(S3_ACCESS_KEY_ENV, ""),
        "aws_secret_access_key": aws_secret_access_key or os.environ.get(S3_SECRET_KEY_ENV, ""),
        "aws_session_token": aws_session_token or os.environ.get(S3_SESSION_TOKEN_ENV, ""),
    }


def create_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    max_retries: int = 3,
) -> Any:
    """
    Create an Amazon S3 boto3 client using resolved credentials and configuration.
    Uses AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    creds = get_credentials(aws_access_key_id, aws_secret_access_key, aws_session_token)
    config = get_s3_config(region=region, endpoint_url=endpoint_url, max_retries=max_retries)

    kwargs = {
        "region_name": region or os.environ.get(S3_REGION_ENV, DEFAULT_REGION),
        "config": config,
    }
    # Only add credentials if they are non-empty
    if creds["aws_access_key_id"]:
        kwargs["aws_access_key_id"] = creds["aws_access_key_id"]
    if creds["aws_secret_access_key"]:
        kwargs["aws_secret_access_key"] = creds["aws_secret_access_key"]
    if creds["aws_session_token"]:
        kwargs["aws_session_token"] = creds["aws_session_token"]

    final_endpoint = endpoint_url or os.environ.get(S3_ENDPOINT_URL_ENV)
    if final_endpoint:
        kwargs["endpoint_url"] = final_endpoint

    return boto3.client("s3", **kwargs)


def create_s3_resource(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> Any:
    """Create an Amazon S3 boto3 resource for higher-level operations."""
    creds = get_credentials(aws_access_key_id, aws_secret_access_key)
    config = get_s3_config(region=region, endpoint_url=endpoint_url)

    kwargs = {
        "region_name": region or os.environ.get(S3_REGION_ENV, DEFAULT_REGION),
        "config": config,
    }
    if creds["aws_access_key_id"]:
        kwargs["aws_access_key_id"] = creds["aws_access_key_id"]
    if creds["aws_secret_access_key"]:
        kwargs["aws_secret_access_key"] = creds["aws_secret_access_key"]

    final_endpoint = endpoint_url or os.environ.get(S3_ENDPOINT_URL_ENV)
    if final_endpoint:
        kwargs["endpoint_url"] = final_endpoint

    return boto3.resource("s3", **kwargs)


def read_file_as_bytes(file_path: str) -> bytes:
    """Read a local file and return its bytes content."""
    with open(file_path, "rb") as f:
        return f.read()


def bytes_to_fileobj(data: bytes) -> io.BytesIO:
    """Convert bytes to a file-like object for upload."""
    return io.BytesIO(data)


def get_content_type(file_path: str) -> str:
    """Determine content type based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    content_types = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".tiff": "image/tiff",
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".json": "application/json",
        ".xml": "application/xml",
        ".html": "text/html",
        ".zip": "application/zip",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return content_types.get(ext, "application/octet-stream")


def handle_s3_error(error: ClientError, operation: str) -> str:
    """Format an S3 ClientError into a descriptive error string."""
    code = error.response.get("Error", {}).get("Code", "Unknown")
    message = error.response.get("Error", {}).get("Message", str(error))
    return f"S3 {operation} error [{code}]: {message}"


def ensure_bucket_exists(
    client: Any,
    bucket: str,
    region: Optional[str] = None,
) -> bool:
    """Check if an S3 bucket exists and optionally create it."""
    try:
        client.head_bucket(Bucket=bucket)
        return True
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchBucket"):
            create_kwargs: Dict[str, Any] = {"Bucket": bucket}
            actual_region = region or os.environ.get(S3_REGION_ENV, DEFAULT_REGION)
            if actual_region != "us-east-1":
                create_kwargs["CreateBucketConfiguration"] = {
                    "LocationConstraint": actual_region
                }
            client.create_bucket(**create_kwargs)
            return True
        raise
