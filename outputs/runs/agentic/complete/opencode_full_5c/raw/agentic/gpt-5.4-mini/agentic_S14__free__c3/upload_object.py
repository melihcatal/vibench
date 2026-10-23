from typing import Any, Optional

from storage_client import build_upload_response, get_s3_client
from storage_models import UploadObjectRequest


def upload_object(
    bucket: str,
    key: str,
    body: Any,
    content_type: Optional[str] = None,
    metadata: Optional[dict] = None,
):
    client = get_s3_client()
    request = UploadObjectRequest(
        bucket=bucket, key=key, body=body, content_type=content_type, metadata=metadata
    )
    kwargs = {"Bucket": request.bucket, "Key": request.key, "Body": request.body}
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    if request.metadata:
        kwargs["Metadata"] = request.metadata
    result = client.put_object(**kwargs)
    return build_upload_response(request.bucket, request.key, result)
