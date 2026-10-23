import boto3
import os
from typing import Optional
from storage_models import StorageConfig, UploadRequest, ObjectMetadata


def get_s3_client():
    """
    Get configured S3 client using environment variables.

    Returns:
        boto3 S3 client
    """
    # Use AWS credentials from environment
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
    return boto3.client("s3")


def get_s3_resource():
    """
    Get configured S3 resource using environment variables.

    Returns:
        boto3 S3 resource
    """
    return boto3.resource("s3")


def load_storage_config() -> StorageConfig:
    """
    Load storage configuration from environment variables.

    Returns:
        StorageConfig: Configuration object
    """
    return StorageConfig(
        provider="Amazon S3",
        bucket_name=os.getenv("AWS_S3_BUCKET", ""),
        region=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        access_key_id=os.getenv("AWS_ACCESS_KEY_ID", ""),
        secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
        endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL", None),
    )


def normalize_upload_request(
    file_path: Optional[str] = None,
    data_bytes: Optional[bytes] = None,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> UploadRequest:
    """
    Normalize upload request parameters.

    Args:
        file_path: Path to local file
        data_bytes: Bytes data
        content_type: MIME type
        metadata: User metadata

    Returns:
        UploadRequest: Normalized request
    """
    if file_path and not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path and not data_bytes:
        raise ValueError("Either file_path or data_bytes must be provided")

    # Auto-detect content type if not provided
    if file_path and not content_type:
        import mimetypes

        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

    return UploadRequest(
        file_path=file_path,
        data_bytes=data_bytes,
        content_type=content_type or "application/octet-stream",
        metadata=metadata or {},
    )


def parse_s3_metadata(head_response: dict) -> ObjectMetadata:
    """
    Parse S3 head_object response into normalized metadata.

    Args:
        head_response: S3 head_object response

    Returns:
        ObjectMetadata: Normalized metadata
    """
    return ObjectMetadata(
        content_length=head_response.get("ContentLength"),
        content_type=head_response.get("ContentType"),
        last_modified=head_response.get("LastModified"),
        etag=head_response.get("ETag"),
        storage_class=head_response.get("StorageClass", "STANDARD"),
        user_metadata=head_response.get("Metadata", {}),
        server_side_encryption=head_response.get("ServerSideEncryption"),
        version_id=head_response.get("VersionId"),
    )
