import os
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import StorageClient
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    file_path: Optional[str] = None,
    data: Optional[bytes] = None,
    content_type: Optional[str] = None,
    metadata: Optional[dict[str, str]] = None,
    storage_class: str = "STANDARD",
    server_side_encryption: Optional[str] = None,
    tags: Optional[dict[str, str]] = None,
) -> UploadResponse:
    if not file_path and data is None:
        raise ValueError("Either file_path or data must be provided")
    if not key:
        if file_path:
            key = os.path.basename(file_path)
        else:
            raise ValueError("key must be provided when uploading raw bytes")

    client = StorageClient()
    target_bucket = bucket or client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    resolved_content_type = content_type
    if not resolved_content_type and file_path:
        import mimetypes

        resolved_content_type, _ = mimetypes.guess_type(file_path)
        if resolved_content_type is None:
            resolved_content_type = "application/octet-stream"

    upload_kwargs = {
        "Bucket": target_bucket,
        "Key": key,
        "ContentType": resolved_content_type or "application/octet-stream",
        "StorageClass": storage_class,
    }

    if metadata:
        upload_kwargs["Metadata"] = metadata

    if server_side_encryption:
        upload_kwargs["ServerSideEncryption"] = server_side_encryption

    if tags:
        tag_string = "&".join(f"{k}={v}" for k, v in tags.items())
        upload_kwargs["Tagging"] = tag_string

    try:
        if file_path:
            upload_kwargs["Body"] = open(file_path, "rb")
            try:
                response = client.s3_client.put_object(**upload_kwargs)
            finally:
                upload_kwargs["Body"].close()
        else:
            from io import BytesIO

            upload_kwargs["Body"] = BytesIO(data)
            response = client.s3_client.put_object(**upload_kwargs)

        return UploadResponse.from_s3_response(target_bucket, key, response)

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise RuntimeError(
            f"Amazon S3 upload failed for s3://{target_bucket}/{key}: "
            f"[{error_code}] {error_message}"
        ) from e
