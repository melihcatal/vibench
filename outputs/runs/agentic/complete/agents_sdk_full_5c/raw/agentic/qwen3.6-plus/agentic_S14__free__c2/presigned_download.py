"""
Create a time-limited signed download URL for a stored object (AWS S3).

Uses boto3 S3 presigned URL generation with configurable expiry and response headers.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from botocore.exceptions import ClientError

from storage_client import get_s3_client, get_bucket_name, DEFAULT_PRESIGNED_URL_EXPIRY, validate_object_key
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def generate_presigned_download_url(
    key: str,
    bucket: Optional[str] = None,
    expiry_seconds: Optional[int] = None,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
    s3_client=None,
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for downloading an S3 object.

    Args:
        key: S3 object key (path within the bucket)
        bucket: Target S3 bucket name
        expiry_seconds: URL validity duration in seconds
        response_content_disposition: Override Content-Disposition header
        response_content_type: Override Content-Type header
        s3_client: Pre-configured boto3 S3 client

    Returns:
        PresignedUrlResponse with the generated URL and metadata
    """
    validate_object_key(key)
    bucket_name = get_bucket_name(bucket)
    client = s3_client or get_s3_client()
    expiry = expiry_seconds if expiry_seconds is not None else DEFAULT_PRESIGNED_URL_EXPIRY

    presigned_req = PresignedUrlRequest(
        bucket=bucket_name,
        key=key,
        expiry_seconds=expiry,
        response_content_disposition=response_content_disposition,
        response_content_type=response_content_type,
    )

    params: Dict[str, Any] = {
        "Bucket": presigned_req.bucket,
        "Key": presigned_req.key,
        "ExpiresIn": presigned_req.expiry_seconds,
    }

    response_params: Dict[str, Any] = {}
    if presigned_req.response_content_disposition:
        response_params["ResponseContentDisposition"] = presigned_req.response_content_disposition
    if presigned_req.response_content_type:
        response_params["ResponseContentType"] = presigned_req.response_content_type

    if response_params:
        params["ResponseContentDisposition"] = response_params.get("ResponseContentDisposition")
        params["ResponseContentType"] = response_params.get("ResponseContentType")

    try:
        url = client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=presigned_req.expiry_seconds,
            HttpMethod="GET",
        )

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=presigned_req.expiry_seconds)

        return PresignedUrlResponse(
            url=url,
            bucket=presigned_req.bucket,
            key=presigned_req.key,
            expires_at=expires_at,
            method="GET",
        )

    except ClientError as e:
        raise RuntimeError(
            f"Failed to generate presigned URL for s3://{presigned_req.bucket}/{presigned_req.key}: {e}"
        ) from e


def generate_presigned_urls_for_keys(
    keys: list,
    bucket: Optional[str] = None,
    expiry_seconds: Optional[int] = None,
    s3_client=None,
) -> list:
    """
    Generate presigned URLs for multiple objects.

    Args:
        keys: List of S3 object keys
        bucket: Target S3 bucket name
        expiry_seconds: URL validity duration in seconds
        s3_client: Pre-configured boto3 S3 client

    Returns:
        List of PresignedUrlResponse objects
    """
    return [
        generate_presigned_download_url(
            key=k,
            bucket=bucket,
            expiry_seconds=expiry_seconds,
            s3_client=s3_client,
        )
        for k in keys
    ]
