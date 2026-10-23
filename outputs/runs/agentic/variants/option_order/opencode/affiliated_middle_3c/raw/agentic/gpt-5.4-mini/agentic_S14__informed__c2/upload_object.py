import os
from io import BytesIO
from storage_client import get_bucket
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(bucket_name: str, object_name: str, body, content_type: str | None = None, metadata: dict | None = None) -> UploadObjectResponse:
    bucket = get_bucket(bucket_name)
    req = UploadObjectRequest(object_name=object_name, body=body, content_type=content_type, metadata=metadata)
    if isinstance(req.body, (bytes, bytearray)):
        data = BytesIO(req.body)
    elif hasattr(req.body, 'read'):
        data = req.body
    else:
        data = BytesIO(str(req.body).encode('utf-8'))
    blob = bucket.blob(req.object_name)
    if req.content_type:
        blob.content_type = req.content_type
    if req.metadata:
        blob.metadata = req.metadata
    blob.upload_from_file(data)
    return UploadObjectResponse(bucket_name=bucket_name, object_name=object_name, etag=getattr(blob, 'etag', None), generation=getattr(blob, 'generation', None))
