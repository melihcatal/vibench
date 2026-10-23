import boto3
from botocore.exceptions import ClientError
from storage_client import get_s3_client
from storage_models import PresignedUrlRequest, PresignedUrlResponse
import datetime


def create_presigned_download_url(
    bucket_name: str, object_key: str, expiration_seconds: int = 3600
) -> PresignedUrlResponse:
    """
    Creates a time-limited signed download URL for a stored object in AWS S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket
        expiration_seconds: URL expiration time in seconds (default: 1 hour)

    Returns:
        PresignedUrlResponse with signed URL and expiration details
    """
    s3_client = get_s3_client()

    try:
        # Generate presigned URL for GET operation
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration_seconds,
        )

        expiration_time = datetime.datetime.now() + datetime.timedelta(
            seconds=expiration_seconds
        )

        return PresignedUrlResponse(
            success=True,
            url=url,
            bucket=bucket_name,
            key=object_key,
            expiration_seconds=expiration_seconds,
            expiration_time=expiration_time.isoformat(),
            provider="aws_s3",
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False, error_message=str(e), provider="aws_s3"
        )


def create_presigned_upload_url(
    bucket_name: str,
    object_key: str,
    expiration_seconds: int = 3600,
    content_type: str = "application/octet-stream",
) -> PresignedUrlResponse:
    """
    Creates a time-limited signed upload URL for AWS S3.

    Args:
        bucket_name: S3 bucket name
        object_key: Object key (path) in the bucket
        expiration_seconds: URL expiration time in seconds (default: 1 hour)
        content_type: Expected content type of the uploaded object

    Returns:
        PresignedUrlResponse with signed URL and expiration details
    """
    s3_client = get_s3_client()

    try:
        # Generate presigned URL for PUT operation
        url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=expiration_seconds,
        )

        expiration_time = datetime.datetime.now() + datetime.timedelta(
            seconds=expiration_seconds
        )

        return PresignedUrlResponse(
            success=True,
            url=url,
            bucket=bucket_name,
            key=object_key,
            expiration_seconds=expiration_seconds,
            expiration_time=expiration_time.isoformat(),
            content_type=content_type,
            provider="aws_s3",
        )

    except ClientError as e:
        return PresignedUrlResponse(
            success=False, error_message=str(e), provider="aws_s3"
        )


if __name__ == "__main__":
    # Example usage for download URL
    request = PresignedUrlRequest(
        bucket="my-example-bucket", key="test/example.txt", expiration_seconds=1800
    )
    result = create_presigned_download_url(
        request.bucket, request.key, request.expiration_seconds
    )
    print(f"Presigned URL result: {result.success}")
    if result.success:
        print(f"Signed URL: {result.url}")
        print(f"Expires at: {result.expiration_time}")
