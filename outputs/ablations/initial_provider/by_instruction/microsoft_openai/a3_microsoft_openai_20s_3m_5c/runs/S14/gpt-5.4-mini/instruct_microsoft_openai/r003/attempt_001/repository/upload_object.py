from azure.storage.blob import ContentSettings

from storage_client import get_blob_service_client, get_container_name, normalize_bytes
from storage_models import UploadRequest


def upload_object(request: UploadRequest):
    client = get_blob_service_client()
    container_name = get_container_name(request.container_name)
    blob_client = client.get_blob_client(container=container_name, blob=request.object_name)
    payload = normalize_bytes(request.content)
    kwargs = {}
    if request.content_type:
        kwargs["content_settings"] = ContentSettings(content_type=request.content_type)
    if request.metadata:
        kwargs["metadata"] = request.metadata
    return blob_client.upload_blob(payload, overwrite=True, **kwargs)
