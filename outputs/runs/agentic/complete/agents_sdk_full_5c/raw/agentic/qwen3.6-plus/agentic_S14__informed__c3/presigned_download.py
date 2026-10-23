"""
Create a time-limited signed download URL for an object stored in Amazon S3.

Uses boto3 SDK for Amazon S3 (service=Amazon S3).
Environment variables: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from datetime import datetime, timedelta
from typing import Optional

from storage_client import get_s3_client, validate_bucket_name, build_object_key
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def generate_presigned_download_url(
    bucket: str,
    object_key: str,
    expiration_seconds: int = 3600,
    prefix: Optional[str] = None,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedUrlResponse:
    """
    Generate a time-limited presigned URL for downloading an S3 object.

    Args:
        bucket: The S3 bucket name.
        object_key: The S3 object key.
        expiration_seconds: URL validity duration in seconds (default 3600 = 1 hour).
        prefix: Optional prefix to prepend to the object key.
        response_content_disposition: Optional Content-Disposition override for the download response.
        response_content_type: Optional Content-Type override for the download response.

    Returns:
        PresignedUrlResponse containing the signed URL and metadata.

    Raises:
        ValueError: If bucket name is invalid or expiration is out of range.
        ClientError: On S3 API errors.
    """
    validate_bucket_name(bucket)

    if expiration_seconds <= 0:
        raise ValueError("expiration_seconds must be a positive integer")
    if expiration_seconds > 604800:
        raise ValueError(
            "expiration_seconds cannot exceed 604800 (7 days) for S3 presigned URLs"
        )

    if prefix:
        object_key = build_object_key(prefix, object_key)

    request = PresignedUrlRequest(
        bucket=bucket,
        object_key=object_key,
        expiration_seconds=expiration_seconds,
        http_method="GET",
    )

    s3_client = get_s3_client()

    params = {
        "Bucket": bucket,
        "Key": object_key,
        "ExpiresIn": expiration_seconds,
        "HttpMethod": "GET",
    }

    # Optional response headers to override on download
    response_params = {}
    if response_content_disposition:
        response_params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        response_params["ResponseContentType"] = response_content_type

    if response_params:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket,
                "Key": object_key,
                **response_params,
            },
            ExpiresIn=expiration_seconds,
            HttpMethod="GET",
        )
    else:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": object_key},
            ExpiresIn=expiration_seconds,
            HttpMethod="GET",
        )

    expires_at = datetime.utcnow() + timedelta(seconds=expiration_seconds)

    return PresignedUrlResponse(
        url=url,
        bucket=bucket,
        object_key=object_key,
        expires_at=expires_at,
        http_method="GET",
    )
