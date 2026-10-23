import io
from typing import Union, BinaryIO, Dict, Optional

from storage_client import get_s3_client, get_bucket_name
from storage_models import UploadRequest, UploadResponse


def upload_object(
    key: str,
    data: Union[bytes, BinaryIO, io.IOBase],
    content_type: str = "application/octet-stream",
    metadata: Optional[Dict[str, str]] = None,
    bucket: Optional[str] = None,
    storage_class: str = "STANDARD",
    tags: Optional[Dict[str, str]] = None,
) -> UploadResponse:
    if bucket is None:
        bucket = get_bucket_name()

    s3_client = get_s3_client()

    upload_kwargs = {
        "Bucket": bucket,
        "Key": key,
        "ContentType": content_type,
        "StorageClass": storage_class,
    }

    if metadata:
        upload_kwargs["Metadata"] = metadata

    if tags:
        tag_string = "&".join(f"{k}={v}" for k, v in tags.items())
        upload_kwargs["Tagging"] = tag_string

    try:
        if isinstance(data, bytes):
            upload_kwargs["Body"] = io.BytesIO(data)
        else:
            upload_kwargs["Body"] = data

        response = s3_client.put_object(**upload_kwargs)

        return UploadResponse(
            success=True,
            object_key=key,
            bucket=bucket,
            etag=response.get("ETag", "").strip('"'),
            version_id=response.get("VersionId"),
        )
    except Exception as exc:
        return UploadResponse(
            success=False,
            object_key=key,
            bucket=bucket,
            error=str(exc),
        )
