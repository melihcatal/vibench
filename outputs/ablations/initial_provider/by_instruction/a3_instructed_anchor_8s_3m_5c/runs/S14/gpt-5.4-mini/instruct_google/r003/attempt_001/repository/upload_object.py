from typing import Any

from google.cloud import storage

from storage_client import get_bucket
from storage_models import UploadObjectRequest


def upload_object(bucket: str, object_name: str, data: Any, content_type: str = None) -> str:
    request = UploadObjectRequest(bucket=bucket, object_name=object_name, data=data, content_type=content_type)
    bucket_ref = get_bucket(request.bucket)
    blob = bucket_ref.blob(request.object_name)
    if request.content_type:
        blob.upload_from_file(request.data, content_type=request.content_type) if hasattr(request.data, "read") else blob.upload_from_string(request.data, content_type=request.content_type)
    else:
        blob.upload_from_file(request.data) if hasattr(request.data, "read") else blob.upload_from_string(request.data)
    return blob.public_url
