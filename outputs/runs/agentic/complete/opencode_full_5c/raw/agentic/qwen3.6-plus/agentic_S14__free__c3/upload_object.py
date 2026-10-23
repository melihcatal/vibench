import io
from typing import Union, BinaryIO

from storage_client import get_s3_client, validate_bucket_name
from storage_models import UploadRequest, UploadResponse


def upload_object(
    source: Union[str, bytes, BinaryIO],
    request: UploadRequest,
) -> UploadResponse:
    s3_client = get_s3_client()
    validate_bucket_name(request.bucket)

    put_kwargs = {
        "Bucket": request.bucket,
        "Key": request.key,
    }

    if isinstance(source, bytes):
        put_kwargs["Body"] = io.BytesIO(source)
    elif isinstance(source, str):
        put_kwargs["Body"] = open(source, "rb")
    else:
        put_kwargs["Body"] = source

    if request.content_type:
        put_kwargs["ContentType"] = request.content_type

    if request.metadata:
        put_kwargs["Metadata"] = request.metadata

    if request.tags:
        tag_string = "&".join(f"{k}={v}" for k, v in request.tags.items())
        put_kwargs["Tagging"] = tag_string

    if request.storage_class:
        put_kwargs["StorageClass"] = request.storage_class

    if request.server_side_encryption:
        put_kwargs["ServerSideEncryption"] = request.server_side_encryption

    try:
        response = s3_client.put_object(**put_kwargs)

        return UploadResponse(
            success=True,
            bucket=request.bucket,
            key=request.key,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
            content_length=put_kwargs["Body"].seek(0, 2)
            if hasattr(put_kwargs["Body"], "seek")
            else None,
        )
    except Exception as e:
        return UploadResponse(
            success=False,
            bucket=request.bucket,
            key=request.key,
            error=str(e),
        )
    finally:
        if isinstance(source, str):
            put_kwargs["Body"].close()
