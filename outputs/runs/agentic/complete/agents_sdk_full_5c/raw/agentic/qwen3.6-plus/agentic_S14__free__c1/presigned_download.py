"""Create a time-limited presigned download URL for an object in AWS S3.

Uses boto3 (AWS SDK for Python) to generate presigned URLs for Amazon S3 objects.
Requires AWS credentials in environment variables:
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
"""

from datetime import timedelta
from storage_client import get_s3_client, validate_bucket_name
from storage_models import PresignedUrlResult


def presigned_download(bucket, key, expires_in=3600, region=None,
                       endpoint_url=None, http_method="GET",
                       response_content_disposition=None,
                       response_content_type=None):
    """Generate a presigned URL for downloading an S3 object.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        expires_in: URL validity duration in seconds (default 3600 = 1 hour).
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.
        http_method: HTTP method for the presigned URL (default "GET").
        response_content_disposition: Optional Content-Disposition header override.
        response_content_type: Optional Content-Type header override.

    Returns:
        PresignedUrlResult containing the generated URL and metadata.

    Raises:
        botocore.exceptions.ClientError: If URL generation fails.
        ValueError: If expires_in exceeds 604800 seconds (7 days, AWS max).
    """
    validate_bucket_name(bucket)

    max_expiration = 604800  # 7 days in seconds - AWS S3 limit
    if expires_in > max_expiration:
        raise ValueError(
            f"expires_in cannot exceed {max_expiration} seconds (7 days), "
            f"which is the maximum allowed by AWS S3"
        )

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    params = {
        "Bucket": bucket,
        "Key": key,
        "Method": http_method,
        "ExpiresIn": expires_in,
    }

    response_headers = {}
    if response_content_disposition:
        response_headers["ResponseContentDisposition"] = response_content_disposition
    if response_content_type:
        response_headers["ResponseContentType"] = response_content_type

    if response_headers:
        params["ExtraParams"] = response_headers

    url = s3_client.generate_presigned_url(**params)

    return PresignedUrlResult(
        url=url,
        bucket=bucket,
        key=key,
        expires_in=expires_in,
        method=http_method,
    )


def presigned_upload(bucket, key, expires_in=3600, content_type=None,
                     region=None, endpoint_url=None):
    """Generate a presigned URL for uploading to an S3 object key.

    Args:
        bucket: S3 bucket name.
        key: Object key (path within the bucket).
        expires_in: URL validity duration in seconds (default 3600).
        content_type: Expected MIME type for the upload.
        region: Optional AWS region override.
        endpoint_url: Optional custom S3 endpoint.

    Returns:
        PresignedUrlResult containing the generated URL and metadata.
    """
    validate_bucket_name(bucket)

    s3_client = get_s3_client(region=region, endpoint_url=endpoint_url)

    params = {
        "Bucket": bucket,
        "Key": key,
        "Method": "PUT",
        "ExpiresIn": expires_in,
    }

    if content_type:
        params["ExtraParams"] = {"ContentType": content_type}

    url = s3_client.generate_presigned_url(**params)

    return PresignedUrlResult(
        url=url,
        bucket=bucket,
        key=key,
        expires_in=expires_in,
        method="PUT",
    )
