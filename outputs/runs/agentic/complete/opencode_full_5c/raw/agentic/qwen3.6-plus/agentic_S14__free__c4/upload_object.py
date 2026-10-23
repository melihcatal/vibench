import os
from typing import Optional
from storage_client import get_s3_client, validate_bucket_name, validate_object_key
from storage_models import UploadRequest, UploadResponse, normalize_metadata_keys


def upload_object(request: UploadRequest) -> UploadResponse:
    if not validate_bucket_name(request.bucket):
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Invalid bucket name: {request.bucket}",
        )

    if not validate_object_key(request.key):
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=f"Invalid object key: {request.key}",
        )

    if request.body is None and request.file_path is None:
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message="Either body or file_path must be provided",
        )

    s3_client = get_s3_client()

    put_kwargs = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    if request.file_path:
        with open(request.file_path, "rb") as f:
            body_data = f.read()
    else:
        body_data = request.body

    put_kwargs["Body"] = body_data

    if request.content_type:
        put_kwargs["ContentType"] = request.content_type

    if request.metadata:
        put_kwargs["Metadata"] = normalize_metadata_keys(request.metadata)

    if request.storage_class:
        put_kwargs["StorageClass"] = request.storage_class.value

    if request.acl:
        put_kwargs["ACL"] = request.acl.value

    if request.server_side_encryption:
        put_kwargs["ServerSideEncryption"] = request.server_side_encryption

    if request.tags:
        tag_string = "&".join(f"{k}={v}" for k, v in request.tags.items())
        put_kwargs["Tagging"] = tag_string

    try:
        response = s3_client.put_object(**put_kwargs)

        content_length = len(body_data) if body_data else 0

        return UploadResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            storage_class=request.storage_class.value,
            content_length=content_length,
        )
    except Exception as e:
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error_message=str(e),
        )


def upload_bytes(
    bucket: str,
    key: str,
    data: bytes,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> UploadResponse:
    request = UploadRequest(
        bucket=bucket,
        key=key,
        body=data,
        content_type=content_type,
        metadata=metadata or {},
    )
    return upload_object(request)


def upload_file(
    bucket: str,
    key: str,
    file_path: str,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> UploadResponse:
    request = UploadRequest(
        bucket=bucket,
        key=key,
        file_path=file_path,
        content_type=content_type,
        metadata=metadata or {},
    )
    return upload_object(request)
