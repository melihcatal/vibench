"""
presigned_download.py - Creates a time-limited signed download URL for a stored object.

Uses Amazon S3 via boto3 as the concrete managed object storage provider.
Authentication via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
"""

from datetime import timedelta
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import get_s3_client
from storage_models import PresignedUrlResponse


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expires_in: int = 3600,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for downloading an object from Amazon S3.

    The URL is valid for the specified duration and allows anyone with the URL
    to download the object without AWS credentials.

    Args:
        bucket_name: S3 bucket containing the object.
        object_key: S3 object key to generate a download URL for.
        expires_in: URL expiration time in seconds (default: 3600 / 1 hour).
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.
        response_content_disposition: Optional Content-Disposition header override.
        response_content_type: Optional Content-Type header override.

    Returns:
        PresignedUrlResponse containing the generated URL and metadata.

    Raises:
        RuntimeError: If URL generation fails.
    """
    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    extra_params = {}

    if response_content_disposition:
        extra_params["ResponseContentDisposition"] = response_content_disposition

    if response_content_type:
        extra_params["ResponseContentType"] = response_content_type

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_key,
                **extra_params,
            },
            ExpiresIn=expires_in,
            HttpMethod="GET",
        )

        return PresignedUrlResponse(
            url=url,
            bucket_name=bucket_name,
            object_key=object_key,
            expires_in_seconds=expires_in,
            http_method="GET",
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        raise RuntimeError(
            f"Failed to generate presigned download URL from S3: {error_code} - {e}"
        ) from e


def create_presigned_upload_url(
    bucket_name: str,
    object_key: str,
    expires_in: int = 3600,
    content_type: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    region_name: Optional[str] = None,
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for uploading an object to Amazon S3.

    The URL is valid for the specified duration and allows anyone with the URL
    to upload content to the specified key without AWS credentials.

    Args:
        bucket_name: Target S3 bucket.
        object_key: S3 object key to generate an upload URL for.
        expires_in: URL expiration time in seconds (default: 3600 / 1 hour).
        content_type: Optional Content-Type to enforce on upload.
        aws_access_key_id: Optional AWS access key ID.
        aws_secret_access_key: Optional AWS secret access key.
        region_name: Optional AWS region name.

    Returns:
        PresignedUrlResponse containing the generated URL and metadata.

    Raises:
        RuntimeError: If URL generation fails.
    """
    s3_client = get_s3_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    params = {
        "Bucket": bucket_name,
        "Key": object_key,
    }

    if content_type:
        params["ContentType"] = content_type

    try:
        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params=params,
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )

        return PresignedUrlResponse(
            url=url,
            bucket_name=bucket_name,
            object_key=object_key,
            expires_in_seconds=expires_in,
            http_method="PUT",
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        raise RuntimeError(
            f"Failed to generate presigned upload URL for S3: {error_code} - {e}"
        ) from e
