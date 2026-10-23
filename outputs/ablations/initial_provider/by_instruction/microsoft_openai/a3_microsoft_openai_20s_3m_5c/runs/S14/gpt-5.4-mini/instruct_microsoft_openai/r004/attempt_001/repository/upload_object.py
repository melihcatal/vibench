from typing import Union

from azure.storage.blob import ContentSettings

from storage_client import get_blob_client
from storage_models import StorageUploadRequest, normalize_object_name


def upload_object(bucket: str, object_name: str, content: Union[bytes, bytearray, str], content_type: str = None):
    request = StorageUploadRequest(bucket=bucket, object_name=normalize_object_name(object_name), content=content, content_type=content_type)
    blob_client = get_blob_client(request.bucket, request.object_name)
    data = request.content.encode() if isinstance(request.content, str) else request.content
    kwargs = {}
    if request.content_type:
        kwargs["content_settings"] = ContentSettings(content_type=request.content_type)
    return blob_client.upload_blob(data, overwrite=True, **kwargs)
