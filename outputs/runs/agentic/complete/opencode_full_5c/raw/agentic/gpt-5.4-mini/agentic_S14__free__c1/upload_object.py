from typing import Any

from storage_client import create_s3_client, resolve_bucket
from storage_models import ObjectUploadRequest, normalize_object_result


def upload_object(
    bucket: str, key: str, body: Any, content_type: str = None, metadata=None
):
    request = ObjectUploadRequest(
        bucket=bucket, key=key, body=body, content_type=content_type, metadata=metadata
    ).normalize()
    s3 = create_s3_client()
    kwargs = {
        "Bucket": resolve_bucket(request.bucket),
        "Key": request.key,
        "Body": request.body,
    }
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    if request.metadata:
        kwargs["Metadata"] = request.metadata
    response = s3.put_object(**kwargs)
    return normalize_object_result(
        {
            "bucket": kwargs["Bucket"],
            "key": request.key,
            "etag": response.get("ETag"),
            "version_id": response.get("VersionId"),
            "content_type": request.content_type,
            "metadata": request.metadata or {},
        }
    )
