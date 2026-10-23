import os
import oss2
from storage_client import get_oss_bucket, normalize_object_key, build_oss_headers
from storage_models import StorageUploadRequest, StorageUploadResponse


def upload_object(
    bucket_name: str,
    object_key: str,
    file_path: str = None,
    data: bytes = None,
    content_type: str = None,
    metadata: dict = None,
    storage_class: str = None,
) -> StorageUploadResponse:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    headers = build_oss_headers()
    if content_type:
        headers["Content-Type"] = content_type
    if storage_class:
        headers["x-oss-storage-class"] = storage_class

    object_meta = {}
    if metadata:
        for k, v in metadata.items():
            object_meta[k] = v

    try:
        if file_path and os.path.isfile(file_path):
            result = bucket.put_object_from_file(
                object_key, file_path, headers=headers, metadata=object_meta
            )
            size = os.path.getsize(file_path)
        elif data is not None:
            result = bucket.put_object(
                object_key, data, headers=headers, metadata=object_meta
            )
            size = len(data)
        else:
            return StorageUploadResponse(
                success=False,
                object_key=object_key,
                bucket=bucket_name,
                error="No file_path or data provided",
            )

        return StorageUploadResponse(
            success=True,
            object_key=object_key,
            bucket=bucket_name,
            etag=result.etag if hasattr(result, "etag") else None,
            version_id=result.versionid if hasattr(result, "versionid") else None,
            size=size,
        )
    except oss2.exceptions.OssError as e:
        return StorageUploadResponse(
            success=False,
            object_key=object_key,
            bucket=bucket_name,
            error=str(e),
        )
