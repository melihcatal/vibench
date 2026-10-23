import base64
from typing import Optional, Union

from storage_client import get_s3_client
from storage_models import StorageObjectRequest, StorageObjectResult, normalize_body


def upload_object(bucket: str, key: str, body: Optional[Union[bytes, str]] = None, content_type: Optional[str] = None, metadata: Optional[dict] = None, region: Optional[str] = None) -> StorageObjectResult:
    request = StorageObjectRequest(bucket=bucket, key=key, body=normalize_body(body), content_type=content_type, metadata=metadata)
    s3 = get_s3_client(region)
    kwargs = {"Bucket": request.bucket, "Key": request.key, "Body": request.body or b""}
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    if request.metadata:
        kwargs["Metadata"] = request.metadata
    response = s3.put_object(**kwargs)
    return StorageObjectResult(bucket=request.bucket, key=request.key, etag=response.get("ETag"), version_id=response.get("VersionId"))


def upload_object_from_base64(bucket: str, key: str, data_base64: str, content_type: Optional[str] = None, metadata: Optional[dict] = None, region: Optional[str] = None) -> StorageObjectResult:
    return upload_object(bucket, key, base64.b64decode(data_base64), content_type=content_type, metadata=metadata, region=region)
