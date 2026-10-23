from datetime import datetime, timezone
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import StorageClient
from storage_models import PresignedUrlResponse


def create_presigned_download_url(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    expires_in: int = 3600,
    version_id: Optional[str] = None,
    response_content_disposition: Optional[str] = None,
    response_content_type: Optional[str] = None,
) -> PresignedUrlResponse:
    if not key:
        raise ValueError("key is required to generate a presigned download URL")

    client = StorageClient()
    target_bucket = bucket or client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    extra_params = {}

    if version_id:
        extra_params["VersionId"] = version_id

    if response_content_disposition:
        extra_params["ResponseContentDisposition"] = response_content_disposition

    if response_content_type:
        extra_params["ResponseContentType"] = response_content_type

    try:
        url = client.s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": target_bucket,
                "Key": key,
                **extra_params,
            },
            ExpiresIn=expires_in,
            HttpMethod="GET",
        )

        return PresignedUrlResponse(
            bucket=target_bucket,
            key=key,
            url=url,
            expires_in=expires_in,
            http_method="GET",
            generated_at=datetime.now(timezone.utc),
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise RuntimeError(
            f"Amazon S3 presigned URL generation failed for s3://{target_bucket}/{key}: "
            f"[{error_code}] {error_message}"
        ) from e


def create_presigned_upload_url(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    expires_in: int = 3600,
    content_type: Optional[str] = None,
    storage_class: Optional[str] = None,
    server_side_encryption: Optional[str] = None,
) -> PresignedUrlResponse:
    if not key:
        raise ValueError("key is required to generate a presigned upload URL")

    client = StorageClient()
    target_bucket = bucket or client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    extra_params = {}

    if content_type:
        extra_params["ContentType"] = content_type

    if storage_class:
        extra_params["StorageClass"] = storage_class

    if server_side_encryption:
        extra_params["ServerSideEncryption"] = server_side_encryption

    try:
        url = client.s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": target_bucket,
                "Key": key,
                **extra_params,
            },
            ExpiresIn=expires_in,
            HttpMethod="PUT",
        )

        return PresignedUrlResponse(
            bucket=target_bucket,
            key=key,
            url=url,
            expires_in=expires_in,
            http_method="PUT",
            generated_at=datetime.now(timezone.utc),
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise RuntimeError(
            f"Amazon S3 presigned upload URL generation failed for s3://{target_bucket}/{key}: "
            f"[{error_code}] {error_message}"
        ) from e
