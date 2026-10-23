"""
Create a time-limited presigned download URL for an object in Amazon S3.

Uses the boto3 SDK to generate presigned URLs that allow temporary,
authenticated access to objects stored in Amazon Simple Storage Service (S3).
Credentials are resolved from AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
or the default AWS credential chain.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

from storage_client import create_s3_client, validate_bucket_exists
from storage_models import PresignedUrlRequest, PresignedUrlResponse

logger = logging.getLogger(__name__)

# Amazon S3 presigned URL maximum expiration is 7 days (604800 seconds)
_MAX_PRESIGNED_EXPIRY = 604800


def generate_presigned_download_url(
    bucket: str,
    key: str,
    *,
    expires_in_seconds: int = 3600,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
    s3_client: Optional[boto3.client] = None,
) -> PresignedUrlResponse:
    """
    Generate a time-limited presigned URL for downloading an S3 object.

    Args:
        bucket: S3 bucket containing the object.
        key: Object key within the bucket.
        expires_in_seconds: URL validity duration in seconds (max 604800 for S3).
        response_content_disposition: Optional Content-Disposition override.
        response_content_type: Optional Content-Type override.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        PresignedUrlResponse with the generated URL and expiration time.

    Raises:
        ValueError: If the bucket doesn't exist or expiration exceeds S3 limit.
        ClientError: On S3 API failure.
    """
    if expires_in_seconds <= 0:
        raise ValueError("expires_in_seconds must be positive.")
    if expires_in_seconds > _MAX_PRESIGNED_EXPIRY:
        raise ValueError(
            f"Amazon S3 presigned URL expiry cannot exceed {_MAX_PRESIGNED_EXPIRY} seconds (7 days)."
        )

    client = s3_client or create_s3_client()

    if not validate_bucket_exists(client, bucket):
        raise ValueError(f"Bucket '{bucket}' does not exist or is not accessible.")

    extra_params: dict[str, str] = {}
    if response_content_disposition:
        extra_params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        extra_params["ResponseContentType"] = response_content_type

    request = PresignedUrlRequest(
        bucket=bucket,
        key=key,
        method="GET",
        expires_in_seconds=expires_in_seconds,
        response_content_disposition=response_content_disposition,
        response_content_type=response_content_type,
    )

    try:
        url = client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": request.bucket,
                "Key": request.key,
                **extra_params,
            },
            ExpiresIn=request.expires_in_seconds,
            HttpMethod="GET",
        )
    except ClientError as exc:
        logger.error(
            "Failed to generate presigned URL for s3://%s/%s: %s",
            bucket,
            key,
            exc,
        )
        raise

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)

    result = PresignedUrlResponse(
        url=url,
        bucket=bucket,
        key=key,
        expires_at=expires_at,
        method="GET",
    )
    logger.info(
        "Generated presigned download URL for s3://%s/%s (expires in %ds)",
        bucket,
        key,
        expires_in_seconds,
    )
    return result


def generate_presigned_download_url_with_override(
    bucket: str,
    key: str,
    *,
    expires_in_seconds: int = 3600,
    filename: Optional[str] = None,
    content_type: Optional[str] = None,
    cache_control: Optional[str] = None,
    s3_client: Optional[boto3.client] = None,
) -> PresignedUrlResponse:
    """
    Generate a presigned download URL with response-header overrides.

    Useful for forcing a specific download filename or content type
    at download time without modifying the stored object metadata.

    Args:
        bucket: S3 bucket name.
        key: Object key within the bucket.
        expires_in_seconds: URL validity in seconds.
        filename: Download filename (sets Content-Disposition).
        content_type: Content-Type override for the download.
        cache_control: Cache-Control override for the download.
        s3_client: Optional pre-created boto3 S3 client.

    Returns:
        PresignedUrlResponse with the presigned URL.
    """
    from storage_models import build_content_disposition

    disposition = None
    if filename:
        disposition = build_content_disposition(filename)

    return generate_presigned_download_url(
        bucket=bucket,
        key=key,
        expires_in_seconds=expires_in_seconds,
        response_content_disposition=disposition,
        response_content_type=content_type,
        s3_client=s3_client,
    )
