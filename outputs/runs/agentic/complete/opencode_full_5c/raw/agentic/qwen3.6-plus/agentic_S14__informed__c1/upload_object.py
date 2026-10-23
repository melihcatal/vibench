import os
from typing import Union, BinaryIO

from storage_client import get_s3_client, validate_bucket_name, validate_object_key
from storage_models import UploadRequest, UploadResponse


def upload_object(
    bucket: str,
    key: str,
    data: Union[bytes, BinaryIO, None] = None,
    file_path: str = None,
    content_type: str = None,
    metadata: dict = None,
    storage_class: str = "STANDARD",
    tags: dict = None,
) -> UploadResponse:
    client = get_s3_client()
    validate_bucket_name(bucket)
    validate_object_key(key)

    extra_args = {}

    if content_type:
        extra_args["ContentType"] = content_type

    if metadata:
        extra_args["Metadata"] = metadata

    if storage_class and storage_class != "STANDARD":
        extra_args["StorageClass"] = storage_class

    if tags:
        tag_string = "&".join(f"{k}={v}" for k, v in tags.items())
        extra_args["Tagging"] = tag_string

    try:
        if file_path:
            with open(file_path, "rb") as f:
                file_data = f.read()
                response = client.put_object(
                    Bucket=bucket,
                    Key=key,
                    Body=file_data,
                    **extra_args,
                )
                content_length = len(file_data)
        elif data is not None:
            if isinstance(data, bytes):
                content_length = len(data)
            else:
                data.seek(0, os.SEEK_END)
                content_length = data.tell()
                data.seek(0)
            response = client.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
                **extra_args,
            )
        else:
            return UploadResponse(
                success=False,
                bucket=bucket,
                key=key,
                error="Either data or file_path must be provided",
            )

        return UploadResponse(
            success=True,
            bucket=bucket,
            key=key,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            content_length=content_length,
        )

    except Exception as exc:
        return UploadResponse(
            success=False,
            bucket=bucket,
            key=key,
            error=str(exc),
        )


def upload_from_request(request: UploadRequest) -> UploadResponse:
    return upload_object(
        bucket=request.bucket,
        key=request.key,
        data=request.data,
        file_path=request.file_path,
        content_type=request.content_type,
        metadata=request.metadata,
        storage_class=request.storage_class,
        tags=request.tags,
    )
