from typing import BinaryIO, Optional, Union

from storage_client import get_bucket, raise_storage_error
from storage_models import UploadRequest, to_dict


def upload_object(
    bucket: str,
    key: str,
    body: Union[bytes, bytearray, BinaryIO],
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
):
    request = UploadRequest(
        bucket=bucket,
        key=key,
        body=body if isinstance(body, (bytes, bytearray)) else body.read(),
        content_type=content_type,
        metadata=metadata or {},
    )
    try:
        extra_args = {}
        if request.content_type:
            extra_args["ContentType"] = request.content_type
        if request.metadata:
            extra_args["Metadata"] = request.metadata
        get_bucket(request.bucket).put_object(Key=request.key, Body=request.body, **extra_args)
        return to_dict(request)
    except Exception as exc:
        raise raise_storage_error(exc)
