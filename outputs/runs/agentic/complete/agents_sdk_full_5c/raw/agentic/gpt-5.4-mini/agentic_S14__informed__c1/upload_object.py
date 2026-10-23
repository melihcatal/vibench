from pathlib import Path
from typing import BinaryIO, Optional, Union

from google.cloud import storage

from storage_client import get_bucket, load_config
from storage_models import UploadRequest


def upload_object(
    source: Union[str, bytes, BinaryIO],
    object_name: str,
    bucket_name: Optional[str] = None,
    content_type: Optional[str] = None,
) -> str:
    request = UploadRequest(bucket_name=bucket_name, object_name=object_name, content_type=content_type)
    bucket = get_bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if isinstance(source, bytes):
        blob.upload_from_string(source, content_type=request.content_type)
    elif isinstance(source, str):
        path = Path(source)
        blob.upload_from_filename(str(path), content_type=request.content_type)
    else:
        blob.upload_from_file(source, rewind=True, content_type=request.content_type)

    return blob.public_url
