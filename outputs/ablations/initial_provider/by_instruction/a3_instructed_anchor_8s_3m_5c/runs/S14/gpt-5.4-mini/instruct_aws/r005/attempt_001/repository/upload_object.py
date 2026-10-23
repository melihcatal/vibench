import io
from typing import Union

from storage_client import get_bucket_name, get_s3_client
from storage_models import UploadResult, normalize_object_key


def upload_object(key: str, body: Union[str, bytes, io.BufferedIOBase], bucket: str = None, content_type: str = None) -> UploadResult:
    s3 = get_s3_client()
    bucket_name = get_bucket_name(bucket)
    object_key = normalize_object_key(key)
    kwargs = {"Bucket": bucket_name, "Key": object_key, "Body": body}
    if content_type:
        kwargs["ContentType"] = content_type
    response = s3.put_object(**kwargs)
    return UploadResult(bucket=bucket_name, key=object_key, etag=response.get("ETag", ""), version_id=response.get("VersionId"))
