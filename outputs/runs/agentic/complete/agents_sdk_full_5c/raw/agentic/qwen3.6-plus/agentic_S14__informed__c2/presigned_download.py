"""
presigned_download.py - Create a time-limited signed download URL for an
object stored in Amazon S3 managed object storage.

Uses the boto3 SDK (Amazon S3).
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from botocore.exceptions import ClientError, ParamValidationError

from storage_client import create_s3_client, handle_s3_error
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def presigned_download(
    bucket: str,
    key: str,
    expiration_seconds: int = 3600,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region: Optional[str] = None,
    endpoint_url: Optional[str] = None,
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for downloading an object from Amazon S3.

    The URL is valid for a limited time (expiration_seconds) and allows
    anyone with the URL to download the object without S3 credentials.

    Args:
        bucket: S3 bucket name containing the object.
        key: Object key (path) within the bucket.
        expiration_seconds: URL validity duration in seconds (default 3600).
        response_content_disposition: Optional Content-Disposition header override.
        response_content_type: Optional Content-Type header override.
        aws_access_key_id: Optional AWS access key ID override.
        aws_secret_access_key: Optional AWS secret access key override.
        region: Optional AWS region override.
        endpoint_url: Optional S3 endpoint URL override.

    Returns:
        PresignedUrlResponse with the presigned URL and metadata.

    Raises:
        ValueError: If the presigned URL cannot be generated.
    """
    request = PresignedUrlRequest(
        bucket=bucket,
        key=key,
        expiration_seconds=expiration_seconds,
        response_content_disposition=response_content_disposition,
        response_content_type=response_content_type,
    )

    client = create_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region=region,
        endpoint_url=endpoint_url,
    )

    # Build ExtraArgs for response header overrides
    extra_args = {}
    if request.response_content_disposition:
        extra_args["ResponseContentDisposition"] = request.response_content_disposition
    if request.response_content_type:
        extra_args["ResponseContentType"] = request.response_content_type

    try:
        # Generate the presigned URL using boto3 generate_presigned_url
        if extra_args:
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": request.bucket,
                    "Key": request.key,
                    **extra_args,
                },
                ExpiresIn=request.expiration_seconds,
                HttpMethod="GET",
            )
        else:
            url = client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": request.bucket,
                    "Key": request.key,
                },
                ExpiresIn=request.expiration_seconds,
                HttpMethod="GET",
            )

        expires_at = datetime.now(timezone.utc) + timedelta(seconds=request.expiration_seconds)

        return PresignedUrlResponse(
            url=url,
            bucket=request.bucket,
            key=request.key,
            expires_at=expires_at,
            http_method="GET",
        )

    except ParamValidationError as e:
        raise ValueError(f"Invalid parameters for S3 presigned URL: {e}")
    except ClientError as e:
        raise ValueError(handle_s3_error(e, "presigned_download"))
