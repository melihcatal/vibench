import io
from typing import Any, Optional

from storage_client import get_bucket_name, get_s3_client
from storage_models import StorageObjectInput, normalize_upload_result


def upload_object(
    bucket: Optional[str],
    key: str,
    body: Any,
    content_type: Optional[str] = None,
    metadata=None,
):
    client = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    payload = (
        body
        if hasattr(body, "read")
        else io.BytesIO(
            body if isinstance(body, (bytes, bytearray)) else str(body).encode()
        )
    )
    args = {"Bucket": bucket_name, "Key": key, "Body": payload}
    if content_type:
        args["ContentType"] = content_type
    if metadata:
        args["Metadata"] = metadata
    response = client.put_object(**args)
    return normalize_upload_result(bucket_name, key, response)


def upload_from_input(request: StorageObjectInput):
    return upload_object(
        request.bucket,
        request.key,
        request.body,
        request.content_type,
        request.metadata,
    )
