"""
Create a time-limited signed download URL for a stored object.

Uses AWS S3 (boto3) as the concrete managed object storage provider.
Generates presigned URLs via boto3's presigned URL capabilities.
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import boto3
from botocore.exceptions import ClientError

from storage_client import StorageClient, get_client
from storage_models import PresignedUrlResponse


# AWS S3 presigned URL configuration defaults
DEFAULT_EXPIRES_IN = 3600  # 1 hour
MAX_EXPIRES_IN = 604800    # 7 days (AWS maximum)


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in: int = DEFAULT_EXPIRES_IN,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
    response_cache_control: Optional[str] = None,
    version_id: Optional[str] = None,
    client: Optional[StorageClient] = None,
) -> PresignedUrlResponse:
    """
    Generate a presigned download URL for an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        expires_in: URL validity duration in seconds (max 604800).
        response_content_disposition: Content-Disposition header override.
        response_content_type: Content-Type header override.
        response_cache_control: Cache-Control header override.
        version_id: Specific object version for versioned buckets.
        client: Optional pre-configured StorageClient instance.

    Returns:
        PresignedUrlResponse containing the signed URL and metadata.

    Raises:
        ValueError: If expires_in exceeds AWS maximum.
        ClientError: If presigned URL generation fails.
    """
    if expires_in > MAX_EXPIRES_IN:
        raise ValueError(
            f"expires_in cannot exceed {MAX_EXPIRES_IN} seconds "
            f"(AWS S3 maximum). Provided: {expires_in}"
        )

    if expires_in <= 0:
        raise ValueError("expires_in must be a positive integer")

    if client is None:
        client = get_client()

    s3_client = client.get_s3_client()

    params = {
        "Bucket": bucket,
        "Key": key,
        "ExpiresIn": expires_in,
        "HttpMethod": "GET",
    }

    extra_params = {}
    if response_content_disposition:
        extra_params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        extra_params["ResponseContentType"] = response_content_type
    if response_cache_control:
        extra_params["ResponseCacheControl"] = response_cache_control
    if version_id:
        extra_params["VersionId"] = version_id

    if extra_params:
        params["ExtraArgs"] = extra_params

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket,
                "Key": key,
                **extra_params,
            },
            ExpiresIn=expires_in,
            HttpMethod="GET",
        )
    except ClientError as e:
        raise ClientError(
            e.response,
            f"Failed to generate presigned URL for s3://{bucket}/{key}: {e}",
        )

    now_utc = datetime.now(timezone.utc)
    expires_at = now_utc + timedelta(seconds=expires_in)

    return PresignedUrlResponse(
        url=url,
        bucket=bucket,
        key=key,
        expires_in=expires_in,
        http_method="GET",
        generated_at=now_utc,
        expires_at=expires_at,
    )


def create_presigned_upload_url(
    bucket: str,
    key: str,
    expires_in: int = DEFAULT_EXPIRES_IN,
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    client: Optional[StorageClient] = None,
) -> PresignedUrlResponse:
    """
    Generate a presigned upload URL for clients to PUT objects to S3.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        expires_in: URL validity duration in seconds.
        content_type: Expected Content-Type for the upload.
        metadata: User metadata to attach.
        client: Optional pre-configured StorageClient instance.

    Returns:
        PresignedUrlResponse containing the signed upload URL.
    """
    if client is None:
        client = get_client()

    s3_client = client.get_s3_client()

    params: Dict = {"Bucket": bucket, "Key": key}
    if content_type:
        params["ContentType"] = content_type
    if metadata:
        for mk, mv in metadata.items():
            meta_key = mk if mk.startswith("x-amz-meta-") else f"x-amz-meta-{mk}"
            params[meta_key] = mv

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )
    except ClientError as e:
        raise ClientError(
            e.response,
            f"Failed to generate presigned upload URL for s3://{bucket}/{key}: {e}",
        )

    now_utc = datetime.now(timezone.utc)
    expires_at = now_utc + timedelta(seconds=expires_in)

    return PresignedUrlResponse(
        url=url,
        bucket=bucket,
        key=key,
        expires_in=expires_in,
        http_method="PUT",
        generated_at=now_utc,
        expires_at=expires_at,
    )
