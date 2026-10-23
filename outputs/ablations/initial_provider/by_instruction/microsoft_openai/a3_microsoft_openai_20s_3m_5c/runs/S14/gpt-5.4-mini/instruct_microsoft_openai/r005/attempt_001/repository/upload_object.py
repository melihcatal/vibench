from typing import Any, Optional

from azure.storage.blob import ContentSettings

from storage_client import build_blob_service_client, normalize_container_name
from storage_models import UploadRequest


def upload_object(container_name: Optional[str], blob_name: str, data: Any, overwrite: bool = True, content_type: Optional[str] = None):
    client = build_blob_service_client()
    container = normalize_container_name(container_name)
    request = UploadRequest(container_name=container, blob_name=blob_name, data=data, overwrite=overwrite, content_type=content_type)
    blob_client = client.get_blob_client(container=request.container_name, blob=request.blob_name)
    kwargs = {"overwrite": request.overwrite}
    if request.content_type:
        kwargs["content_settings"] = ContentSettings(content_type=request.content_type)
    if hasattr(request.data, "read"):
        return blob_client.upload_blob(request.data, **kwargs)
    return blob_client.upload_blob(request.data, **kwargs)
