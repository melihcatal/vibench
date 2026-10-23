from typing import Any

from storage_client import get_default_bucket, get_s3_client
from storage_models import StorageObjectRequest, normalize_key


def upload_object(
    bucket: str, key: str, body: Any, content_type: str = None, metadata=None
):
    client = get_s3_client()
    req = StorageObjectRequest(
        bucket=bucket,
        key=normalize_key(key),
        body=body,
        content_type=content_type,
        metadata=metadata,
    )
    kwargs = {"Bucket": req.bucket, "Key": req.key, "Body": req.body}
    if req.content_type:
        kwargs["ContentType"] = req.content_type
    if req.metadata:
        kwargs["Metadata"] = req.metadata
    return client.put_object(**kwargs)


def upload_to_default_bucket(
    key: str, body: Any, content_type: str = None, metadata=None
):
    return upload_object(
        get_default_bucket(), key, body, content_type=content_type, metadata=metadata
    )
