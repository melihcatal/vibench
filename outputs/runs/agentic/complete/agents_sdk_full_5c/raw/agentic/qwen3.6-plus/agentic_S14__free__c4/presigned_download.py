"""Create a time-limited signed download URL for a stored object in AWS S3."""

from typing import Optional

from storage_client import S3ClientFactory
from storage_models import PresignedUrlRequest, PresignedUrlResponse


def create_presigned_download_url(
    key: str,
    bucket: Optional[str] = None,
    expiration_seconds: int = 3600,
    http_method: str = "GET",
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for downloading an object from S3.

    Uses boto3's generate_presigned_url method which produces a URL
    signed with AWS SigV4 credentials. The URL grants temporary access
    to the specified S3 object (hosted at s3.amazonaws.com or the
    configured S3_ENDPOINT_URL) without exposing permanent credentials.

    Args:
        key: The object key (path) within the bucket.
        bucket: S3 bucket name (falls back to S3_BUCKET_NAME env var).
        expiration_seconds: URL validity duration in seconds (max 604800 / 7 days).
        http_method: HTTP method for the presigned request (GET, HEAD, etc.).

    Returns:
        PresignedUrlResponse containing the signed URL and metadata.

    Raises:
        botocore.exceptions.ClientError: If the object or bucket is not accessible.
        ValueError: If expiration exceeds 7 days (AWS S3 limit).
    """
    if expiration_seconds > 604800:
        raise ValueError(
            "S3 presigned URLs cannot exceed 604800 seconds (7 days). "
            f"Requested: {expiration_seconds}s"
        )

    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket

    request = PresignedUrlRequest(
        bucket=target_bucket,
        key=key,
        expiration_seconds=expiration_seconds,
        http_method=http_method,
    )

    s3_client = factory.s3_client

    params = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=request.expiration_seconds,
        HttpMethod=request.http_method,
    )

    return PresignedUrlResponse(
        url=url,
        key=request.key,
        bucket=request.bucket,
        expires_in=request.expiration_seconds,
        http_method=request.http_method,
    )


def create_presigned_upload_url(
    key: str,
    bucket: Optional[str] = None,
    expiration_seconds: int = 3600,
    content_type: str = "application/octet-stream",
) -> PresignedUrlResponse:
    """
    Generate a presigned URL for uploading an object to S3.

    Allows a client to upload directly to S3 without holding AWS credentials.
    The upload is scoped to the specific key and content type.

    Args:
        key: The object key (path) where the upload will be stored.
        bucket: S3 bucket name.
        expiration_seconds: URL validity in seconds.
        content_type: Expected MIME type of the uploaded content.

    Returns:
        PresignedUrlResponse with a PUT-signed URL.
    """
    factory = S3ClientFactory(bucket=bucket)
    target_bucket = factory.bucket

    s3_client = factory.s3_client

    params = {
        "Bucket": target_bucket,
        "Key": key,
        "ContentType": content_type,
    }

    url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params=params,
        ExpiresIn=expiration_seconds,
        HttpMethod="PUT",
    )

    return PresignedUrlResponse(
        url=url,
        key=key,
        bucket=target_bucket,
        expires_in=expiration_seconds,
        http_method="PUT",
    )
