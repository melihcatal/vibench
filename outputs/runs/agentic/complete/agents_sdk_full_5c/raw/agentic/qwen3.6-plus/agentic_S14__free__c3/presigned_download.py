"""
Create a time-limited signed download URL for a stored object (AWS S3).

Provider: AWS S3 via boto3
- Uses boto3 S3 client generate_presigned_url for AWS S3 presigned URLs
- AWS S3 endpoint: https://s3.{region}.amazonaws.com
- Provider-specific method: generate_presigned_url('get_object', ...)
"""

import logging
from typing import Optional

from storage_client import get_s3_client
from storage_models import PresignedURLRequest, PresignedURLResponse

logger = logging.getLogger(__name__)


def create_presigned_download_url(
    bucket: str,
    key: str,
    expires_in_seconds: int = 3600,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedURLResponse:
    """
    Generate a presigned URL for downloading an object from AWS S3.

    The URL is valid for the specified duration and can be shared
    with unauthenticated clients for time-limited access.

    Provider signals:
    - boto3 S3 client (AWS S3 managed object storage)
    - generate_presigned_url is an AWS S3-specific SDK method
    - AWS S3 presigned URL signing with SigV4
    """
    s3_client = get_s3_client()

    request = PresignedURLRequest(
        bucket=bucket,
        key=key,
        expires_in_seconds=expires_in_seconds,
        http_method="GET",
        response_content_disposition=response_content_disposition,
        response_content_type=response_content_type,
    )

    params = {
        "Bucket": bucket,
        "Key": key,
    }

    if response_content_disposition:
        params["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        params["ResponseContentType"] = response_content_type

    logger.info(
        "Generating presigned URL for s3://%s/%s, expires in %ds",
        bucket, key, expires_in_seconds,
    )

    url = s3_client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=expires_in_seconds,
        HttpMethod="GET",
    )

    return PresignedURLResponse(
        url=url,
        bucket=bucket,
        key=key,
        expires_in_seconds=expires_in_seconds,
        method="GET",
    )
