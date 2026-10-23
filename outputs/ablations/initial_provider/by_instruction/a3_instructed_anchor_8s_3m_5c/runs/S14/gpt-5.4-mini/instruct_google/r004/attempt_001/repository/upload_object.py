import base64
from typing import Any, BinaryIO, Optional, Union

from google.cloud import storage

from storage_client import get_bucket
from storage_models import normalize_object_name, UploadResult


def upload_object(
    bucket_name: str,
    object_name: str,
    data: Union[bytes, bytearray, str, BinaryIO],
    content_type: Optional[str] = None,
) -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    if isinstance(data, str):
        payload: Any = data.encode("utf-8")
    else:
        payload = data
    if hasattr(payload, "read"):
        blob.upload_from_file(payload, content_type=content_type)
    else:
        blob.upload_from_string(payload, content_type=content_type)
    result = UploadResult(
        bucket=bucket_name,
        name=blob.name,
        content_type=blob.content_type,
        size=blob.size,
        md5_hash=base64.b64encode(blob.md5_hash.encode("utf-8")).decode("utf-8") if blob.md5_hash else None,
        generation=blob.generation,
    )
    return result.to_dict()
